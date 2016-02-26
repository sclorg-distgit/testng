%global pkg_name testng
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}


%global group_id  org.testng

Name:             %{?scl_prefix}%{pkg_name}
Version:          6.8.7
Release:          3.13%{?dist}
Summary:          Java-based testing framework
# org/testng/remote/strprotocol/AbstractRemoteTestRunnerClient.java is CPL
License:          ASL 2.0 and CPL
URL:              http://testng.org/
# Source0 was generated using clean-tarball.sh due to possible licensing issues
# with the original
Source0:          %{pkg_name}-%{version}.tar.gz
Source1:          clean-tarball.sh

BuildArch:        noarch

BuildRequires:    %{?scl_prefix}mvn(com.beust:jcommander) >= 1.27
BuildRequires:    %{?scl_prefix_java_common}mvn(com.google.guava:guava)
BuildRequires:    %{?scl_prefix}mvn(com.google.inject:guice)
BuildRequires:    %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:    %{?scl_prefix_java_common}mvn(org.apache.ant:ant)
BuildRequires:    %{?scl_prefix}mvn(org.beanshell:bsh)
BuildRequires:    %{?scl_prefix}mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires:    %{?scl_prefix_java_common}mvn(org.yaml:snakeyaml)

BuildRequires:    %{?scl_prefix}maven-local
BuildRequires:    %{?scl_prefix}maven-plugin-bundle

%description
TestNG is a testing framework inspired from JUnit and NUnit but introducing
some new functionality, including flexible test configuration, and
distributed test running.  It is designed to cover unit tests as well as
functional, end-to-end, integration, etc.

%package javadoc
Summary:          API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# build fix for new guice
%pom_add_dep com.google.guava:guava::provided
sed -i "s|com.google.inject.internal|com.google.common.collect|" \
  src/main/java/org/testng/xml/XmlDependencies.java \
  src/main/java/org/testng/xml/XmlGroups.java \
  src/main/java/org/testng/xml/dom/TestNGTagFactory.java \
  src/test/java/test/dependent/InstanceSkipSampleTest.java \
  src/test/java/test/mustache/MustacheTest.java \
  src/test/java/test/thread/B.java

%pom_remove_plugin :maven-gpg-plugin
%pom_remove_plugin :maven-source-plugin
  
# remove bundled stuff
rm -rf spring
rm -rf 3rdparty
rm -rf lib-supplied
rm -rf gigaspaces
rm -f *.jar

# convert to UTF-8
native2ascii -encoding UTF-8 src/main/java/org/testng/internal/Version.java \
  src/main/java/org/testng/internal/Version.java

iconv --from-code=ISO-8859-2 --to-code=UTF-8 ANNOUNCEMENT.txt > ANNOUNCEMENT.txt.utf8
mv -f ANNOUNCEMENT.txt.utf8 ANNOUNCEMENT.txt

%mvn_file : %{pkg_name}
# jdk15 classifier is used by some other packages
%mvn_alias : :::jdk15:
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build -- -Dgpg.skip=true
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE.txt ANNOUNCEMENT.txt CHANGES.txt README

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 6.8.7-3.13
- Fix BR on maven-local & co.

* Mon Feb 08 2016 Michal Srb <msrb@redhat.com> - 6.8.7-3.12
- Build against snakeyaml from rh-java-common

* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 6.8.7-3.11
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 6.8.7-3.10
- maven33 rebuild

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 6.8.7-3.9
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 6.8.7-3.8
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 6.8.7-3.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.3
- SCL-ize build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8.7-3.1
- First maven30 software collection build

* Thu Jan 23 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6.8.7-3
- Remove test file with unclear licensing from tarball
- Resolves: rhbz#1055931

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.8.7-2
- Mass rebuild 2013-12-27

* Thu Sep 12 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 6.8.7-1
- Update to upstream version 6.8.7
- Provide additional jdk15 classifier

* Tue Aug 27 2013 Michal Srb <msrb@redhat.com> - 6.8-3
- Migrate away from mvn-rpmbuild (Resolves: #997518)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 6.8-2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

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
