%{?scl:%scl_package testng}
%{!?scl:%global pkg_name %{name}}

%bcond_without groovy

Name:           %{?scl_prefix}testng
Version:        6.9.12
Release:        5.1%{?dist}
Summary:        Java-based testing framework
License:        ASL 2.0
URL:            http://testng.org/
Source0:        https://github.com/cbeust/testng/archive/%{version}.tar.gz
Patch0:         0001-Avoid-accidental-javascript-in-javadoc.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.beust:jcommander)
BuildRequires:  %{?scl_prefix}mvn(com.google.inject:guice::no_aop:)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.ant:ant)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.beanshell:bsh)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.yaml:snakeyaml)
%if %{with groovy}
BuildRequires:  %{?scl_prefix}mvn(org.assertj:assertj-core)
BuildRequires:  mvn(org.codehaus.gmavenplus:gmavenplus-plugin)
BuildRequires:  mvn(org.codehaus.groovy:groovy-all)
BuildRequires:  mvn(org.spockframework:spock-core)
%endif

%description
TestNG is a testing framework inspired from JUnit and NUnit but introducing
some new functionality, including flexible test configuration, and
distributed test running.  It is designed to cover unit tests as well as
functional, end-to-end, integration, etc.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}

%patch0 -p1

# remove any bundled libs, but not test resources
find ! -path "*/test/*" -name *.jar -print -delete
find -name *.class -delete

# these are unnecessary
%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-source-plugin
%pom_remove_plugin :maven-javadoc-plugin

# missing test deps
%if %{with groovy}
%pom_add_plugin "org.codehaus.gmavenplus:gmavenplus-plugin" pom.xml \
  "<executions><execution><goals><goal>addTestSources</goal><goal>testGenerateStubs</goal><goal>testCompile</goal><goal>removeTestStubs</goal></goals></execution></executions>"
%pom_add_dep "org.spockframework:spock-core::test"
%pom_add_dep "org.codehaus.groovy:groovy-all::test"
%endif

# avoid SNAPSHOT in version number
sed -i -e '/<version>/s/-SNAPSHOT//' pom.xml

# plugins not in Fedora
%pom_remove_plugin com.coderplus.maven.plugins:copy-rename-maven-plugin
sed -i -e 's/VersionTemplateJava/Version.java/' pom.xml
mv ./src/main/resources/org/testng/internal/VersionTemplateJava ./src/main/resources/org/testng/internal/Version.java

cp -p ./src/main/java/*.dtd.html ./src/main/resources/.


%mvn_file : %{pkg_name}
# jdk15 classifier is used by some other packages
%mvn_alias : :::jdk15:

%build
%if %{with groovy}
%mvn_build -- -Dmaven.local.debug=true
%else
%mvn_build -f -- -Dmaven.local.debug=true
%endif

%install
%mvn_install

%files -f .mfiles
%doc CHANGES.txt README.md
%license LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 6.9.12-5.1
- Automated package import and SCL-ization

* Wed May 31 2017 Michael Simacek <msimacek@redhat.com> - 6.9.12-5
- Avoid accidental javascript in comment

* Fri Feb 17 2017 Mat Booth <mat.booth@redhat.com> - 6.9.12-4
- License correction

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.9.12-2
- Introduce build-conditional to allow building without groovy

* Tue Nov 01 2016 Mat Booth <mat.booth@redhat.com> - 6.9.12-1
- Update to upstream version 6.9.12
- Avoid 'SNAPSHOT' in pom version to fix tests in testng-remote package

* Wed Apr 20 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.9.11-1
- Update to upstream version 6.9.11

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 gil cattaneo <puntogil@libero.it> 6.9.10-1
- Update to 6.9.10

* Tue Oct 27 2015 gil cattaneo <puntogil@libero.it> 6.9.9-1
- Update to 6.9.9

* Tue Oct 13 2015 gil cattaneo <puntogil@libero.it> 6.9.8-1
- Update to 6.9.8

* Mon Sep 07 2015 Mat Booth <mat.booth@redhat.com> - 6.9.5-1
- Update to 6.9.5

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 6.8.21-1
- Update to 6.8.21
- introduce license macro

* Tue Jan 20 2015 gil cattaneo <puntogil@libero.it> 6.8.17-1
- Update to 6.8.17

* Wed Jan 14 2015 gil cattaneo <puntogil@libero.it> 6.8.14-1
- Update to 6.8.14

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.8-3
- Fix build-requires on sonatype-oss-parent

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.8-1
- Update to upstream version 6.8.8

* Thu Sep 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6.8.7-1
- Update to upstream version 6.8.7
- Provide additional jdk15 classifier

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.5-1
- Update to upstream version 6.8.5

* Sun Feb 10 2013 Mat Booth <fedora@matbooth.co.uk> - 6.8-1
- Update to latest upstream release, rhbz #888233

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 6.0.1-6
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 08 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6.0.1-5
- Part of testng is CPL, add it to license tag

* Thu Jul 26 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6.0.1-4
- Spec file cleanups and add_maven_depmap macro use
- Drop no longer needed depmap

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu May 12 2011 Jaromir Capik <jcapik@redhat.com> - 6.0.1-1
- Update to 6.0.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 19 2010 Lubomir Rintel <lkundrak@v3.sk> - 5.11-3
- Drop backport util concurrent dependency, we don't build jdk14 jar

* Mon Dec 21 2009 Lubomir Rintel <lkundrak@v3.sk> - 5.11-2
- Add POM

* Sun Dec 20 2009 Lubomir Rintel <lkundrak@v3.sk> - 5.11-1
- Bump to 5.11
- Add maven depmap fragments
- Fix line encoding of README

* Wed Dec 09 2009 Lubomir Rintel <lkundrak@v3.sk> - 5.10-2
- Add javadoc
- Don't ship jdk14 jar

* Fri Nov 27 2009 Lubomir Rintel <lkundrak@v3.sk> - 5.10-1
- Initial packaging
