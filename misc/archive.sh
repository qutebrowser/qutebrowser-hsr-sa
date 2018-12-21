#!/bin/bash

set -e

abgabedir=~/proj/qutebrowser/sa-private/abgabe
archivedir=$abgabedir/archive
uploaddir=$abgabedir/upload
sadir=~/proj/qutebrowser/sa
saprivate=~/proj/qutebrowser/sa-private

if [[ -d "$abgabedir" ]]; then
    echo "Existing dir found, exiting." >&1
    exit 1
fi
mkdir "$abgabedir"

mkdir "$archivedir"

mkdir "$archivedir/repos"
git clone ~/proj/qutebrowser/git "$archivedir/repos/qutebrowser"
git clone "$sadir" "$archivedir/repos/qutebrowser-hsr-sa"
git clone https://github.com/qutebrowser/qutebrowser-hsr-sa.wiki.git "$archivedir/repos/notes"

cat << EOF > "$archivedir/readme.txt"
qutebrowser code: repos/qutebrowser
SA repository: repos/qutebrowser-hsr-sa
Notizen-Wiki: repos/notes

Unterschriebene Erklärungen: legal/
Sitzungsprotokolle: repos/qutebrowser-hsr-sa/meetings
Aufgabenstellung: repos/qutebrowser-hsr-sa/doc/img/SA_Bruhin_Aufgabenstellung_v2.pdf
EOF

cp "$sadir/doc/main.pdf" "$archivedir/sa-bruhin-qutebrowser.pdf"

mkdir "$archivedir/legal"
cp "$saprivate/eigenstaendigkeit.pdf" "$archivedir/legal"
cp "$saprivate/eigenstaendigkeit.odt" "$archivedir/legal"
cp "$saprivate/urheberrechte.pdf" "$archivedir/legal"
cp "$saprivate/urheberrechte.odt" "$archivedir/legal"
cp "$saprivate/publikation.pdf" "$archivedir/legal"
cp "$saprivate/publikation.odt" "$archivedir/legal"

mkdir "$uploaddir"
ln -s "$archivedir/sa-bruhin-qutebrowser.pdf" "$uploaddir/sa.pdf"
ln -s "$archivedir/repos/qutebrowser-hsr-sa/poster/poster.pdf" "$uploaddir/poster.pdf"
ln -s "$archivedir/legal/eigenstaendigkeit.pdf" "$uploaddir/eigenstaendigkeit.pdf"
ln -s "$archivedir/legal/urheberrechte.pdf" "$uploaddir/urheberrechte.pdf"
ln -s "$archivedir/legal/publikation.pdf" "$uploaddir/publikation.pdf"
ln -s "$archivedir/repos/qutebrowser-hsr-sa/misc/plain-abstract.txt" "$uploaddir/plain-abstract.txt"
zip -r "$uploaddir/archive.zip" "$archivedir"/* 
