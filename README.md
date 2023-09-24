## 1 - Gathering and naming image files (thu thập ảnh chữ)
    python scripts/renameimages.py

## 2 - Generating Box files (Tạo khung bao)
    python scripts/boxfiles.py

## 3 - Annotating Box files (Gắn nhãn)
    jTessBoxEditor
    => https://github.com/nguyenq/jTessBoxEditor/releases/tag/Release-2.3.1
    => Guide: https://miai.vn/2019/08/28/ocr-dao-tao-tesseract-ocr-de-nhan-dang-tieng-viet-voi-cac-font-chu-khu-khoam/

## 4 - Training Tesseract (Huấn luyện tạo model)
    python scripts/train.py

## 5 - Purge before training
    python scripts/purge.py

## 6 - Predict
    tesseract <path-to-image> <path-to-output> --oem 1 -l eng+vie
    tesseract data/prepared/vie.vni.exp1.png ./.out/output --oem 3 -l vie
    tesseract data/prepared/vie.vni.exp1.png stdout --oem 3 -l vie --psm 7

## 7 - List all options
    tesseract --help-extra

## 8 - List all available languages
    tesseract --list-langs

## 8 - References
    https://muthu.co/all-tesseract-ocr-options/