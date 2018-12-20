#!/bin/bash

abgabedir=~/proj/qutebrowser/sa-private/abgabe
archivedir=$abgabedir/archive
uploaddir=$abgabedir/upload
sadir=~/proj/qutebrowser/sa
privatedir=~/proj/qutebrowser/sa-private

if [[ -d "$abgabedir" ]]; then
    echo "Existing dir found, exiting." >&1
    exit 1
fi
mkdir "$abgabedir"

mkdir "$archivedir"

mkdir "$archivedir/repos"
git clone https://github.com/qutebrowser/qutebrowser "$archivedir/repos/qutebrowser"
git clone https://github.com/qutebrowser/qutebrowser-hsr-sa "$archivedir/repos/qutebrowser-hsr-sa"
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
# cp "$sadir/poster/main.pdf" "$archivedir/sa-bruhin-qutebrowser-poster.pdf"
cp "$sadir/misc/plain-abstract.txt" "$archivedir"

mkdir "$archivedir/legal"
cp "$saprivate/eigenstaendigkeit.pdf" "$archivedir/legal"
cp "$saprivate/urheberrechte.pdf" "$archivedir/legal"
cp "$saprivate/publikation.pdf" "$archivedir/legal"

mkdir "$uploaddir"
ln -s "$archivedir/sa-bruhin-qutebrowser.pdf" "$uploaddir/sa.pdf"
ln -s "$archivedir/sa-bruhin-qutebrowser-poster.pdf" "$uploaddir/poster.pdf"
ln -s "$archivedir/legal/eigenstaendigkeit.pdf" "$uploaddir/eigenstaendigkeit.pdf"
ln -s "$archivedir/legal/urheberrechte.pdf" "$uploaddir/urheberrechte.pdf"
ln -s "$archivedir/legal/publikation.pdf" "$uploaddir/publikation.pdf"
ln -s "$archivedir/plain-abstract.txt" "$uploaddir/plain-abstract.txt"
zip -r "$archivedir"/* "$uploaddir/archive.zip"
