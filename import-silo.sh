#! /bin/sh

src="$1"
SUBDIRS="score pdb swat silo debug pdb unknown filters"
rm -Rf src/silo
mkdir -p src/silo/include
cp $src/include/*.h src/silo/include
for i in $SUBDIRS; do
  mkdir -p src/silo/$i
  cp $src/silo/$i/*.{c,h} src/silo/$i
done
