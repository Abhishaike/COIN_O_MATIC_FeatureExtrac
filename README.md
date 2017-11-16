# COIN_O_MATIC_FeatureExtrac

This is a python implementation of the feature extraction technique used in the 2006 paper https://lvdmaaten.github.io/publications/papers/MuscleCIS_2006.pdf, written by L.J.P. van der Maaten and P.J. Boon. 


Example usage:
```
FileNameHolder_Train = ["~/Coin1", "~/Coin2, "~/Coin3"]
Train_X = []
for FileName in FileNameHolder_Train:
    TempCoinHolder = FindCoin(FileName)
    HistogramHolder = SplitIntoConcentric(radius = 250, COIN_IMAGE = TempCoinHolder, Center_Y = 250, Center_X = 250)
    Train_X.append(HistogramHolder)
```

*Do not* change the SplitIntoConcentric() parameters unless you know what you're doing. The FindCoin() function already resizes the image to a 500x500 size, so there is no need to change anything here. 

Near-zero preprocessing is required, the back-end will take care of segmenting the coin, applying the correct filters, and everything else. Bring up an issue if you have any questions/requests. 
