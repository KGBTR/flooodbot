# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
And this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 1 April 2021

### Added

- Added `add-flood`, `make-suggestion` and `report-error` fields

## [1.1.0] - 1 April 2021

### Added

- Added `PY_ENV`. Its required for dont reply in development. Just logging to stdout. Only reply on production.
- 27 floods added:
  -  İntihar
  - Burak Oyunda
  - Hotwheels Sharky
  - Bu ne iğrenç bir grup
  - Pişirmek için aldığım tavuğu siktim
  - Biliyor musun zeynep
  - Çocuklar Duymasın Swinger
  - 60 manat
  - İbne kadı
  - Zımbabwe
  - Sikmek istiyorum
  - Hop ss aldım
  - İki olasılık var
  - Sikmeyin kızları
  - Be amına kodumun salağı
  - Hort beyler
  - Am sikmek istiyorum
  - Kelmange
  - Gitti demi oğlum
  - Yine gelsene
  - Yak albayım
  - Bu saz değil bağlamadır
  - Rezil rüsva orospu çocuğu
  - İzmir belediyesi israfı
  - Türk olmak
  - Makinalaşmak istiyorum
  - 16 saattir otobüsteyim

### Changes

- Configuration file moved into seperate file.
- Reply message moved into seperate markdown template file. Exp: [`FLOOD.md`](template/FLOOD.md), [`LISTING.md`](template/LISTING.md)
- Utility and command functions moved into seperate file.

## [1.0.0] - 29 March 2021

### Added

- Heroku one click deploy button.
- Both support `praw.ini` and `environment variables`(for heroku).
