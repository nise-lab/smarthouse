#!/bin/bash

mkdir julius
cd julius

if [ ! -e julius-4.4.2/julius/julius ]; then
  if [ ! -e julius-4.4.2 ]; then
    if [ ! -e v4.4.2.zip ]; then
      wget https://github.com/julius-speech/julius/archive/v4.4.2.zip
    fi

    unzip v4.4.2.zip
  fi

  cd julius-4.4.2
  ./configure
  make
  cd ..
fi

if [ ! -e dictation-kit-dictation-kit-v4.3.1 ]; then
  if [ ! -e dictation-kit-v4.3.1.zip ]; then
    wget https://github.com/julius-speech/dictation-kit/archive/dictation-kit-v4.3.1.zip
  fi
  unzip dictation-kit-v4.3.1.zip
fi

if [ ! -e dictation-kit-dictation-kit-v4.3.1/bin/osx/_julius ]; then
  mv dictation-kit-dictation-kit-v4.3.1/bin/osx/julius dictation-kit-dictation-kit-v4.3.1/bin/osx/_julius
  cp julius-4.4.2/julius/julius dictation-kit-dictation-kit-v4.3.1/bin/osx/julius
fi

if [ ! -e dictation-kit-dictation-kit-v4.3.1/bin/linux/_julius ]; then
  mv dictation-kit-dictation-kit-v4.3.1/bin/linux/julius dictation-kit-dictation-kit-v4.3.1/bin/linux/_julius
  cp julius-4.4.2/julius/julius dictation-kit-dictation-kit-v4.3.1/bin/linux/julius
fi

if [ ! -e bccwj.60k.htkdic ]; then
  cp dictation-kit-dictation-kit-v4.3.1/model/lang_m/bccwj.60k.htkdic bccwj.60k.htkdic
fi

if [ ! -e jnas-tri-3k16-gid.binhmm ]; then
  cp dictation-kit-dictation-kit-v4.3.1/model/phone_m/jnas-tri-3k16-gid.binhmm jnas-tri-3k16-gid.binhmm
fi

if [ ! -e logicalTri ]; then
  cp dictation-kit-dictation-kit-v4.3.1/model/phone_m/logicalTri logicalTri
fi
