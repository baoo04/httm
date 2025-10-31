import os, shutil, random

IMG_DIR = "dataset/images"
LABEL_DIR = "dataset/labels"
TRAIN_IMG = "dataset/images/train"
TEST_IMG = "dataset/images/test"
TRAIN_LBL = "dataset/labels/train"
TEST_LBL = "dataset/labels/test"

for d in [TRAIN_IMG, TEST_IMG, TRAIN_LBL, TEST_LBL]:
    os.makedirs(d, exist_ok=True)

images = [f for f in os.listdir(IMG_DIR) if f.endswith('.jpg')]
random.shuffle(images)

split_idx = int(0.7 * len(images))
train_files = images[:split_idx]
test_files = images[split_idx:]

for files, img_dest, lbl_dest in [(train_files, TRAIN_IMG, TRAIN_LBL), (test_files, TEST_IMG, TEST_LBL)]:
    for f in files:
        shutil.copy(os.path.join(IMG_DIR, f), os.path.join(img_dest, f))
        label_file = f.replace('.jpg', '.txt')
        shutil.copy(os.path.join(LABEL_DIR, label_file), os.path.join(lbl_dest, label_file))

print(f"✅ Done! Train: {len(train_files)}, Test: {len(test_files)}")
