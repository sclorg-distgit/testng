#!/bin/bash

version=$(grep Version: *spec | sed -e 's/Version:\s*\(.*\)/\1/')

wget https://github.com/cbeust/testng/archive/testng-${version}.tar.gz \
    -O testng-${version}.tar.gz

rm -rf testng-testng-${version}
tar xvf testng-${version}.tar.gz
mv testng-testng-${version} testng-${version}


# TestClass has possible licensing issues so just clean that set of tests
rm -rf testng-${version}/src/test/java/test/preserveorder/

find testng-${version} -iname '*.jar' -delete
find testng-${version} -iname '*.class' -delete

tar cf testng-${version}.tar.gz testng-${version}
