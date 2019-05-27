def correct(x):

    number = x

    l = [16, 17, 20, 21]
    b = [32, 33, 34, 35]
    lbc = [48, 50, 52, 54, 56]
    lb = [49, 51, 53, 55, 57]
    r = [64, 66, 72, 74]
    lr = range(80, 96)
    rbc = [96, 97, 104, 105]
    rb = [98, 99, 106, 107]
    lrb34 = [112, 116, 120, 124]
    lrb4 = [113, 117, 121, 125]
    lrb3 = [114, 118, 122, 126]
    lrb = [115, 119, 123, 127]
    t = [128, 132, 136, 140]
    ltc = [144, 145, 152, 153]
    lt = [148, 149, 156, 157]
    bt = range(160, 176)
    lbt13 = [176, 178, 184, 186]
    lbt1 = [177, 179, 185, 187]
    lbt3 = [180, 182, 188, 190]
    lbt = [181, 183, 189, 191]
    rtc = [192, 194, 196, 198]
    rt = [200, 202, 204, 206]
    lrt12 = [208, 209, 210, 211]
    lrt2 = [212, 213, 214, 215]
    lrt1 = [216, 217, 218, 219]
    lrt = [220, 221, 222, 223]
    rbt24 = [224, 225, 228, 229]
    rbt2 = [226, 227, 230, 231]
    rbt4 = [232, 233, 236, 237]
    rbt = [234, 235, 238, 239]

    basis = [l, b, lbc, lb, r, lr, rbc, rb, lrb34, lrb4, lrb3, lrb, t, ltc, lt, bt, lbt13, lbt1, lbt3, lbt, rtc, rt,
             lrt12, lrt2, lrt1, lrt, rbt24, rbt2, rbt4, rbt]

    for element in basis:
        if number in element:
            number = element[0]
            break

    return number
