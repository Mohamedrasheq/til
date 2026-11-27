# Finding test receipts that also sit in train, without downloading the images

_Learned: 2026-11-27_

**The problem:** the dataset had no official split, so I made my own by id. Later I found the same receipt in both train and test under different ids. That makes the test score too high, and I couldn't tell by how much.

**What worked:** two checks.

1. **Same file.** A zip's central directory already stores a CRC-32 and size for every file. Reading only that index over the Hugging Face file system gives a fingerprint per image, with no image downloaded.
2. **Same receipt, different photo.** Same seller, date and total (all three filled) in two different splits.

The copy in test is kept, then val, then train. The others are dropped from every split. Same-split pairs only get a review list, because two real receipts can match.

```python
from huggingface_hub import HfFileSystem
with HfFileSystem().open(ZIP, "rb", block_size=1 << 20) as f:
    infos = zipfile.ZipFile(f).infolist()          # reads the index, not the images
fingerprint = {Path(i.filename).stem: (i.CRC, i.file_size) for i in infos if not i.is_dir()}
```

The result: 131 test receipts had a byte-identical copy in train or val, and about 100 more matched on seller, date and total. The same index also showed 17 images of 0 bytes.

A test now fails if any kept train receipt matches a kept test receipt on the core fields. It caught one more case: dates printed without a year.

**Why it matters:** an id-based split doesn't protect you from duplicate files. Check content before trusting any test score.
