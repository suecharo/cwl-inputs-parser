# CWL conformance test

テスト用の cwl file として、CWL conformance test を使う。

1. conformance test のうち、所謂クセのない cwl file のみを抽出する (e.g. streamable などがないもの)
2. cwl-utils を用いて、input object を抽出し、更に主要な部分を抽出し json 化する
3. `cwltool --make-template` や conformance test の job file などを参考にしつつ、2. に基づいた workflow parameters の生成方法についての考察をする

- neko-punch の python において、cwl url を input として 2. を生成
- neko-punch の web component において、2. を参考に web form を生成
- neko-punch の web component において、web form の入力から 3. を生成

## Download test

下の yaml に基づいて、tool file と job file を download する

- https://raw.githubusercontent.com/common-workflow-language/common-workflow-language/main/v1.0/conformance_test_v1.0.yaml
- https://raw.githubusercontent.com/common-workflow-language/cwl-v1.1/main/conformance_tests.yaml
- https://raw.githubusercontent.com/common-workflow-language/cwl-v1.2/main/conformance_tests.yaml

```bash=
$ python3 download_test.py v1.0
$ python3 download_test.py v1.1
$ python3 download_test.py v1.2
```

## Choose test

conformance*test*\*.yaml を修正しつつ、test を選択する。
neko-punch として、support しない test を除く。
