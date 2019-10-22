#!/bin/bash
HERE=$(cd $(dirname $0) && echo $PWD)
ICONDIR=$HOME/.local/share/icons
APPDIR=$HOME/.local/share/applications
BINDIR=$HOME/bin

while IFS="|" read _source _target; do
    (mkdir -p "$_target"; cd "$_target"; ln -vs "$_source")
done <<-LINKs
	$HERE/zbarshot.svg|$ICONDIR
	$HERE/zbarshot.desktop|$APPDIR
    $HERE/zbarshot|$BINDIR
LINKs
