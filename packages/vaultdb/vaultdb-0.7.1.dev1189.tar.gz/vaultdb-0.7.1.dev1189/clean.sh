#!/bin/sh

SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

echo $SCRIPTPATH

rm -rf	$SCRIPTPATH/.eggs \
		$SCRIPTPATH/.pytest_cache \
		$SCRIPTPATH/build \
		$SCRIPTPATH/dist \
		$SCRIPTPATH/vaultdb.egg-info \
		$SCRIPTPATH/vaultdb.cpp \
		$SCRIPTPATH/vaultdb.hpp \
		$SCRIPTPATH/parquet-extension.cpp \
		$SCRIPTPATH/parquet-extension.hpp \
		$SCRIPTPATH/vaultdb \
		$SCRIPTPATH/vaultdb_tarball

rm -f	$SCRIPTPATH/sources.list \
		$SCRIPTPATH/includes.list \
		$SCRIPTPATH/githash.list

python3 -m pip uninstall vaultdb --yes
