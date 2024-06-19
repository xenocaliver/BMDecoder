#!/usr/local/sage/default/sage -python
# coding: utf-8

import sys            # for argv function
import random         # import random number functions
from sage.all import *

CHECKBITS = './checkbits.dat'
INJECTFILE = './inject.txt'
CORRECTFILE = './correction_result.txt'
ERRORFILE = './error.dat'
# 40bit Correction BCH Shift Register

def lfsr560(x, indata):

    #initialize y
    y = []
    for i in range(0, 560):
        y.append(0)

    # shift x
    y[559] = x[558]^indata^x[559];
    y[558] = indata^x[559]^x[557]
    y[557] = x[556]
    y[556] = x[555]
    y[555] = x[554]
    y[554] = x[553]
    y[553] = x[552]
    y[552] = x[551]
    y[551] = x[550]
    y[550] = x[549]^indata^x[559]
    y[549] = indata^x[548]^x[559]
    y[548] = indata^x[559]^x[547]
    y[547] = x[546]^indata^x[559]
    y[546] = indata^x[545]^x[559]
    y[545] = indata^x[559]^x[544]
    y[544] = x[543]^indata^x[559]
    y[543] = indata^x[559]^x[542]
    y[542] = x[541]
    y[541] = x[540]
    y[540] = x[539]
    y[539] = indata^x[538]^x[559]
    y[538] = x[537]
    y[537] = x[536]
    y[536] = indata^x[559]^x[535]
    y[535] = x[534]^indata^x[559]
    y[534] = x[533]
    y[533] = indata^x[559]^x[532]
    y[532] = indata^x[559]^x[531]
    y[531] = x[530]
    y[530] = x[529]
    y[529] = x[528]
    y[528] = indata^x[527]^x[559]
    y[527] = indata^x[559]^x[526]
    y[526] = x[525]
    y[525] = x[524]^indata^x[559]
    y[524] = x[523]
    y[523] = x[522]
    y[522] = x[521]
    y[521] = x[520]
    y[520] = x[519]
    y[519] = indata^x[559]^x[518]
    y[518] = x[517]^indata^x[559]
    y[517] = x[516]
    y[516] = indata^x[559]^x[515]
    y[515] = x[514]^indata^x[559]
    y[514] = indata^x[559]^x[513]
    y[513] = x[512]
    y[512] = x[511]
    y[511] = x[510]
    y[510] = indata^x[509]^x[559]
    y[509] = x[508]
    y[508] = x[507]^indata^x[559]
    y[507] = indata^x[559]^x[506]
    y[506] = x[505]^indata^x[559]
    y[505] = x[504]
    y[504] = indata^x[559]^x[503]
    y[503] = x[502]^indata^x[559]
    y[502] = x[501]
    y[501] = x[500]
    y[500] = x[499]^indata^x[559]
    y[499] = x[498]
    y[498] = indata^x[497]^x[559]
    y[497] = indata^x[559]^x[496]
    y[496] = x[495]
    y[495] = x[494]
    y[494] = x[493]^indata^x[559]
    y[493] = indata^x[559]^x[492]
    y[492] = x[491]
    y[491] = x[490]
    y[490] = x[489]
    y[489] = x[488]
    y[488] = indata^x[559]^x[487]
    y[487] = x[486]^indata^x[559]
    y[486] = x[485]
    y[485] = x[484]
    y[484] = x[483]^indata^x[559]
    y[483] = indata^x[559]^x[482]
    y[482] = indata^x[559]^x[481]
    y[481] = indata^x[480]^x[559]
    y[480] = x[479]^indata^x[559]
    y[479] = x[478]
    y[478] = x[477]
    y[477] = x[476]^indata^x[559]
    y[476] = indata^x[475]^x[559]
    y[475] = x[474]
    y[474] = x[473]
    y[473] = indata^x[559]^x[472]
    y[472] = x[471]
    y[471] = x[470]^indata^x[559]
    y[470] = indata^x[559]^x[469]
    y[469] = x[468]
    y[468] = indata^x[559]^x[467]
    y[467] = x[466]
    y[466] = x[465]
    y[465] = x[464]
    y[464] = x[463]
    y[463] = x[462]
    y[462] = indata^x[559]^x[461]
    y[461] = x[460]
    y[460] = x[459]
    y[459] = x[458]^indata^x[559]
    y[458] = x[457]
    y[457] = x[456]
    y[456] = x[455]^indata^x[559]
    y[455] = x[454]
    y[454] = indata^x[453]^x[559]
    y[453] = indata^x[559]^x[452]
    y[452] = x[451]
    y[451] = x[450]
    y[450] = indata^x[559]^x[449]
    y[449] = x[448]^indata^x[559]
    y[448] = x[447]^indata^x[559]
    y[447] = x[446]
    y[446] = indata^x[559]^x[445]
    y[445] = x[444]
    y[444] = indata^x[559]^x[443]
    y[443] = x[442]
    y[442] = indata^x[559]^x[441]
    y[441] = x[440]
    y[440] = x[439]
    y[439] = indata^x[559]^x[438]
    y[438] = x[437]^indata^x[559]
    y[437] = indata^x[559]^x[436]
    y[436] = x[435]^indata^x[559]
    y[435] = x[434]
    y[434] = indata^x[559]^x[433]
    y[433] = x[432]^indata^x[559]
    y[432] = x[431]
    y[431] = indata^x[559]^x[430]
    y[430] = x[429]^indata^x[559]
    y[429] = x[428]
    y[428] = indata^x[559]^x[427]
    y[427] = x[426]^indata^x[559]
    y[426] = indata^x[559]^x[425]
    y[425] = x[424]^indata^x[559]
    y[424] = x[423]
    y[423] = indata^x[422]^x[559]
    y[422] = x[421]
    y[421] = x[420]
    y[420] = x[419]^indata^x[559]
    y[419] = indata^x[559]^x[418]
    y[418] = indata^x[417]^x[559]
    y[417] = x[416]
    y[416] = indata^x[559]^x[415]
    y[415] = x[414]
    y[414] = x[413]^indata^x[559]
    y[413] = x[412]
    y[412] = x[411]
    y[411] = indata^x[559]^x[410]
    y[410] = indata^x[559]^x[409]
    y[409] = indata^x[408]^x[559]
    y[408] = indata^x[559]^x[407]
    y[407] = x[406]^indata^x[559]
    y[406] = x[405]
    y[405] = x[404]
    y[404] = x[403]^indata^x[559]
    y[403] = x[402]
    y[402] = x[401]
    y[401] = indata^x[400]^x[559]
    y[400] = indata^x[559]^x[399]
    y[399] = indata^x[398]^x[559]
    y[398] = indata^x[559]^x[397]
    y[397] = x[396]^indata^x[559]
    y[396] = indata^x[395]^x[559]
    y[395] = x[394]
    y[394] = x[393]^indata^x[559]
    y[393] = x[392]
    y[392] = indata^x[559]^x[391]
    y[391] = x[390]
    y[390] = x[389]
    y[389] = indata^x[559]^x[388]
    y[388] = x[387]
    y[387] = x[386]
    y[386] = indata^x[559]^x[385]
    y[385] = x[384]^indata^x[559]
    y[384] = x[383]^indata^x[559]
    y[383] = x[382]^indata^x[559]
    y[382] = x[381]^indata^x[559]
    y[381] = indata^x[559]^x[380]
    y[380] = x[379]
    y[379] = x[378]^indata^x[559]
    y[378] = indata^x[559]^x[377]
    y[377] = indata^x[376]^x[559]
    y[376] = x[375]^indata^x[559]
    y[375] = x[374]
    y[374] = x[373]
    y[373] = x[372]
    y[372] = indata^x[559]^x[371]
    y[371] = x[370]
    y[370] = x[369]^indata^x[559]
    y[369] = x[368]
    y[368] = x[367]
    y[367] = x[366]^indata^x[559]
    y[366] = indata^x[365]^x[559]
    y[365] = indata^x[559]^x[364]
    y[364] = x[363]
    y[363] = indata^x[559]^x[362]
    y[362] = x[361]^indata^x[559]
    y[361] = indata^x[559]^x[360]
    y[360] = x[359]^indata^x[559]
    y[359] = x[358]^indata^x[559]
    y[358] = x[357]
    y[357] = indata^x[559]^x[356]
    y[356] = indata^x[559]^x[355]
    y[355] = x[354]
    y[354] = x[353]
    y[353] = x[352]
    y[352] = x[351]
    y[351] = x[350]^indata^x[559]
    y[350] = indata^x[559]^x[349]
    y[349] = x[348]^indata^x[559]
    y[348] = x[347]^indata^x[559]
    y[347] = x[346]^indata^x[559]
    y[346] = x[345]^indata^x[559]
    y[345] = x[344]
    y[344] = indata^x[343]^x[559]
    y[343] = x[342]
    y[342] = indata^x[559]^x[341]
    y[341] = x[340]
    y[340] = x[339]^indata^x[559]
    y[339] = x[338]
    y[338] = x[337]
    y[337] = x[336]^indata^x[559]
    y[336] = indata^x[559]^x[335]
    y[335] = x[334]^indata^x[559]
    y[334] = x[333]
    y[333] = x[332]
    y[332] = x[331]^indata^x[559]
    y[331] = indata^x[559]^x[330]
    y[330] = x[329]
    y[329] = x[328]
    y[328] = x[327]^indata^x[559]
    y[327] = x[326]
    y[326] = x[325]
    y[325] = x[324]
    y[324] = indata^x[559]^x[323]
    y[323] = x[322]
    y[322] = indata^x[321]^x[559]
    y[321] = x[320]
    y[320] = indata^x[559]^x[319]
    y[319] = indata^x[318]^x[559]
    y[318] = x[317]
    y[317] = x[316]^indata^x[559]
    y[316] = x[315]
    y[315] = x[314]^indata^x[559]
    y[314] = x[313]
    y[313] = x[312]
    y[312] = x[311]
    y[311] = x[310]
    y[310] = x[309]
    y[309] = indata^x[559]^x[308]
    y[308] = x[307]
    y[307] = indata^x[559]^x[306]
    y[306] = indata^x[559]^x[305]
    y[305] = x[304]
    y[304] = x[303]
    y[303] = x[302]^indata^x[559]
    y[302] = x[301]^indata^x[559]
    y[301] = x[300]
    y[300] = x[299]
    y[299] = indata^x[559]^x[298]
    y[298] = indata^x[559]^x[297]
    y[297] = x[296]
    y[296] = indata^x[295]^x[559]
    y[295] = indata^x[559]^x[294]
    y[294] = x[293]
    y[293] = x[292]
    y[292] = x[291]^indata^x[559]
    y[291] = x[290]
    y[290] = x[289]
    y[289] = x[288]^indata^x[559]
    y[288] = x[287]
    y[287] = x[286]
    y[286] = x[285]^indata^x[559]
    y[285] = x[284]
    y[284] = indata^x[559]^x[283]
    y[283] = x[282]
    y[282] = indata^x[559]^x[281]
    y[281] = x[280]
    y[280] = x[279]^indata^x[559]
    y[279] = x[278]
    y[278] = x[277]
    y[277] = indata^x[559]^x[276]
    y[276] = x[275]
    y[275] = x[274]^indata^x[559]
    y[274] = x[273]
    y[273] = x[272]
    y[272] = x[271]
    y[271] = indata^x[559]^x[270]
    y[270] = x[269]
    y[269] = x[268]
    y[268] = x[267]
    y[267] = x[266]
    y[266] = x[265]
    y[265] = x[264]
    y[264] = x[263]
    y[263] = x[262]
    y[262] = x[261]
    y[261] = indata^x[260]^x[559]
    y[260] = indata^x[259]^x[559]
    y[259] = x[258]
    y[258] = x[257]
    y[257] = x[256]
    y[256] = x[255]
    y[255] = x[254]
    y[254] = indata^x[559]^x[253]
    y[253] = x[252]
    y[252] = x[251]
    y[251] = x[250]
    y[250] = x[249]^indata^x[559]
    y[249] = indata^x[559]^x[248]
    y[248] = indata^x[559]^x[247]
    y[247] = x[246]
    y[246] = indata^x[559]^x[245]
    y[245] = x[244]^indata^x[559]
    y[244] = indata^x[559]^x[243]
    y[243] = indata^x[242]^x[559]
    y[242] = x[241]^indata^x[559]
    y[241] = x[240]
    y[240] = indata^x[559]^x[239]
    y[239] = x[238]^indata^x[559]
    y[238] = x[237]^indata^x[559]
    y[237] = x[236]^indata^x[559]
    y[236] = x[235]
    y[235] = indata^x[559]^x[234]
    y[234] = indata^x[233]^x[559]
    y[233] = indata^x[559]^x[232]
    y[232] = x[231]
    y[231] = x[230]
    y[230] = x[229]
    y[229] = x[228]^indata^x[559]
    y[228] = x[227]^indata^x[559]
    y[227] = indata^x[559]^x[226]
    y[226] = indata^x[559]^x[225]
    y[225] = indata^x[224]^x[559]
    y[224] = indata^x[559]^x[223]
    y[223] = x[222]
    y[222] = x[221]
    y[221] = x[220]^indata^x[559]
    y[220] = x[219]^indata^x[559]
    y[219] = x[218]
    y[218] = x[217]
    y[217] = x[216]^indata^x[559]
    y[216] = indata^x[215]^x[559]
    y[215] = indata^x[559]^x[214]
    y[214] = x[213]
    y[213] = x[212]
    y[212] = x[211]
    y[211] = indata^x[210]^x[559]
    y[210] = x[209]
    y[209] = x[208]^indata^x[559]
    y[208] = x[207]
    y[207] = x[206]
    y[206] = x[205]^indata^x[559]
    y[205] = x[204]
    y[204] = indata^x[559]^x[203]
    y[203] = x[202]^indata^x[559]
    y[202] = x[201]
    y[201] = x[200]
    y[200] = indata^x[559]^x[199]
    y[199] = x[198]^indata^x[559]
    y[198] = indata^x[559]^x[197]
    y[197] = indata^x[196]^x[559]
    y[196] = x[195]
    y[195] = indata^x[559]^x[194]
    y[194] = x[193]^indata^x[559]
    y[193] = x[192]
    y[192] = x[191]
    y[191] = x[190]
    y[190] = x[189]^indata^x[559]
    y[189] = x[188]
    y[188] = indata^x[559]^x[187]
    y[187] = x[186]^indata^x[559]
    y[186] = indata^x[185]^x[559]
    y[185] = indata^x[559]^x[184]
    y[184] = x[183]^indata^x[559]
    y[183] = indata^x[559]^x[182]
    y[182] = x[181]
    y[181] = indata^x[559]^x[180]
    y[180] = x[179]
    y[179] = x[178]
    y[178] = x[177]
    y[177] = x[176]^indata^x[559]
    y[176] = x[175]
    y[175] = x[174]
    y[174] = x[173]
    y[173] = x[172]
    y[172] = indata^x[559]^x[171]
    y[171] = x[170]
    y[170] = x[169]
    y[169] = x[168]
    y[168] = x[167]
    y[167] = indata^x[559]^x[166]
    y[166] = x[165]
    y[165] = x[164]^indata^x[559]
    y[164] = x[163]
    y[163] = indata^x[162]^x[559]
    y[162] = x[161]^indata^x[559]
    y[161] = indata^x[559]^x[160]
    y[160] = x[159]^indata^x[559]
    y[159] = indata^x[559]^x[158]
    y[158] = indata^x[157]^x[559]
    y[157] = x[156]^indata^x[559]
    y[156] = x[155]
    y[155] = x[154]
    y[154] = x[153]
    y[153] = indata^x[152]^x[559]
    y[152] = x[151]
    y[151] = indata^x[559]^x[150]
    y[150] = indata^x[149]^x[559]
    y[149] = indata^x[559]^x[148]
    y[148] = x[147]
    y[147] = indata^x[559]^x[146]
    y[146] = x[145]^indata^x[559]
    y[145] = x[144]^indata^x[559]
    y[144] = indata^x[559]^x[143]
    y[143] = x[142]^indata^x[559]
    y[142] = indata^x[141]^x[559]
    y[141] = x[140]
    y[140] = indata^x[559]^x[139]
    y[139] = x[138]^indata^x[559]
    y[138] = x[137]^indata^x[559]
    y[137] = indata^x[559]^x[136]
    y[136] = indata^x[559]^x[135]
    y[135] = indata^x[134]^x[559]
    y[134] = x[133]
    y[133] = x[132]^indata^x[559]
    y[132] = x[131]
    y[131] = x[130]^indata^x[559]
    y[130] = indata^x[559]^x[129]
    y[129] = x[128]^indata^x[559]
    y[128] = x[127]
    y[127] = x[126]^indata^x[559]
    y[126] = x[125]^indata^x[559]
    y[125] = x[124]
    y[124] = indata^x[123]^x[559]
    y[123] = x[122]
    y[122] = x[121]
    y[121] = x[120]^indata^x[559]
    y[120] = x[119]
    y[119] = x[118]
    y[118] = indata^x[559]^x[117]
    y[117] = x[116]
    y[116] = x[115]
    y[115] = x[114]
    y[114] = x[113]^indata^x[559]
    y[113] = x[112]
    y[112] = x[111]
    y[111] = x[110]^indata^x[559]
    y[110] = x[109]^indata^x[559]
    y[109] = x[108]
    y[108] = indata^x[559]^x[107]
    y[107] = x[106]^indata^x[559]
    y[106] = indata^x[105]^x[559]
    y[105] = indata^x[559]^x[104]
    y[104] = x[103]^indata^x[559]
    y[103] = x[102]
    y[102] = x[101]
    y[101] = x[100]^indata^x[559]
    y[100] = indata^x[559]^x[ 99]
    y[ 99] = x[ 98]
    y[ 98] = x[ 97]
    y[ 97] = x[ 96]
    y[ 96] = x[ 95]^indata^x[559]
    y[ 95] = x[ 94]
    y[ 94] = indata^x[ 93]^x[559]
    y[ 93] = x[ 92]
    y[ 92] = x[ 91]
    y[ 91] = x[ 90]^indata^x[559]
    y[ 90] = indata^x[ 89]^x[559]
    y[ 89] = x[ 88]
    y[ 88] = x[ 87]^indata^x[559]
    y[ 87] = indata^x[559]^x[ 86]
    y[ 86] = x[ 85]
    y[ 85] = indata^x[ 84]^x[559]
    y[ 84] = x[ 83]
    y[ 83] = x[ 82]
    y[ 82] = indata^x[ 81]^x[559]
    y[ 81] = x[ 80]
    y[ 80] = indata^x[ 79]^x[559]
    y[ 79] = x[ 78]
    y[ 78] = x[ 77]
    y[ 77] = x[ 76]
    y[ 76] = x[ 75]
    y[ 75] = x[ 74]
    y[ 74] = indata^x[559]^x[ 73]
    y[ 73] = x[ 72]^indata^x[559]
    y[ 72] = indata^x[ 71]^x[559]
    y[ 71] = x[ 70]
    y[ 70] = x[ 69]^indata^x[559]
    y[ 69] = indata^x[559]^x[ 68]
    y[ 68] = x[ 67]
    y[ 67] = x[ 66]
    y[ 66] = x[ 65]
    y[ 65] = x[ 64]^indata^x[559]
    y[ 64] = x[ 63]
    y[ 63] = indata^x[ 62]^x[559]
    y[ 62] = x[ 61]
    y[ 61] = indata^x[559]^x[ 60]
    y[ 60] = x[ 59]^indata^x[559]
    y[ 59] = x[ 58]
    y[ 58] = indata^x[ 57]^x[559]
    y[ 57] = indata^x[559]^x[ 56]
    y[ 56] = indata^x[559]^x[ 55]
    y[ 55] = x[ 54]
    y[ 54] = x[ 53]
    y[ 53] = x[ 52]^indata^x[559]
    y[ 52] = x[ 51]
    y[ 51] = x[ 50]
    y[ 50] = indata^x[559]^x[ 49]
    y[ 49] = x[ 48]
    y[ 48] = x[ 47]
    y[ 47] = x[ 46]^indata^x[559]
    y[ 46] = x[ 45]
    y[ 45] = x[ 44]^indata^x[559]
    y[ 44] = x[ 43]
    y[ 43] = x[ 42]
    y[ 42] = x[ 41]
    y[ 41] = x[ 40]
    y[ 40] = x[ 39]
    y[ 39] = x[ 38]
    y[ 38] = x[ 37]
    y[ 37] = x[ 36]
    y[ 36] = x[ 35]
    y[ 35] = x[ 34]
    y[ 34] = x[ 33]
    y[ 33] = indata^x[559]^x[ 32]
    y[ 32] = x[ 31]
    y[ 31] = indata^x[ 30]^x[559]
    y[ 30] = x[ 29]
    y[ 29] = x[ 28]
    y[ 28] = indata^x[559]^x[ 27]
    y[ 27] = indata^x[ 26]^x[559]
    y[ 26] = x[ 25]^indata^x[559]
    y[ 25] = x[ 24]
    y[ 24] = x[ 23]
    y[ 23] = x[ 22]^indata^x[559]
    y[ 22] = indata^x[559]^x[ 21]
    y[ 21] = x[ 20]^indata^x[559]
    y[ 20] = x[ 19]
    y[ 19] = x[ 18]^indata^x[559]
    y[ 18] = x[ 17]^indata^x[559]
    y[ 17] = x[ 16]^indata^x[559]
    y[ 16] = x[ 15]^indata^x[559]
    y[ 15] = x[ 14]
    y[ 14] = x[ 13]
    y[ 13] = indata^x[559]^x[ 12]
    y[ 12] = x[ 11]
    y[ 11] = x[ 10]^indata^x[559]
    y[ 10] = x[  9]^indata^x[559]
    y[  9] = x[  8]
    y[  8] = x[  7]^indata^x[559]
    y[  7] = indata^x[559]^x[  6]
    y[  6] = indata^x[559]^x[  5]
    y[  5] = x[  4]
    y[  4] = x[  3]
    y[  3] = x[  2]
    y[  2] = x[  1]
    y[  1] = x[  0]
    y[  0] = indata^x[559]

    return y

######################### generate random bit pattern #################################
def generateData(dimension):
    
    data = []
    for i in range(0, dimension):
        data.append(randint(0, 1))
    
    return data    

########################## End of Function ############################################

def encodeBCH560(indata, BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName):
    
    # generate checkbits list
    checkbits = []
    if BaseElement == 2:
        CheckBitsNumber = MultiplicativeOrder*CorrectableBits
    else:
        CheckBitsNumber = 2*MultiplicativeOrder*CorrectableBits
    for i in range(0, CheckBitsNumber):
        checkbits.append(0)
    
    #check invalid data
    if len(indata) > BaseElement**MultiplicativeOrder - 1:
        print "Invalid Data Size = {0}".format(len(indata))
        sys.exit(1)

    #generate checkbits
    for i in range(0, len(indata)):
        checkbits = lfsr560(checkbits, indata[i])

    #open file and save user data and checkbits
    # open file
    try:
        fp = open(CodeFileName, 'w')
        #write user data to CodeFileName
        for i in range(0, len(indata)):
            fp.write(str(indata[i]))
        
        #write checkbits to CodeFileName
        for i in range(len(checkbits) - 1, -1, -1):
            fp.write(str(checkbits[i]))
            
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(CodeFileName)
        sys.exit()

def checkBCH560(BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName):

    #initialize input data list
    input = []
    CodeWordSize = BaseElement**MultiplicativeOrder - 1
    for i in range(0, CodeWordSize):
        input.append(0)
    #initialize checkbits
    checkbits = []
    if BaseElement == 2:
        CheckBitSize = MultiplicativeOrder*CorrectableBits
    else:
        CheckBitSize = 2*MultiplicativeOrder*CorrectableBits
        
    for i in range(0, CheckBitSize):
        checkbits.append(0)
    #open file and read codeword
    # open file
    try:
        fp = open(CodeFileName, 'r')
        #write user data to CodeFileName
        for i in range(0, CodeWordSize):
            input[i] = int(fp.read(1), 2) #2進数として読み込み
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(CodeFileName)
        sys.exit()
    
    #calculate checkbits with lfsr560
    for i in range(0, len(input)):
        checkbits = lfsr560(checkbits, input[i])

    #open file and write checkbits
    # open file
    try:
        fp = open(CHECKBITS, 'w')
        #write user data to CHECKBITS
        for i in range(CheckBitSize - 1, -1, -1):
            fp.write(str(checkbits[i])) #write data as a character
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(CHECKBITS)
        sys.exit()

def bitflip(x):
    y = 0
    if x == 1:
        y = 0
    else:
        y = 1
    
    return y

def injectErrors(BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName):

    # initialize Galois Field Parameters
    q = BaseElement               # degree of BaseElement
    m = MultiplicativeOrder       # Multiplicative Order of GF(2)
    CodeWordLength = q**m - 1     # Code Word Length
    #initialize input data list
    input = []                    # declare as a list
    for i in range(0, CodeWordLength):  # set 0 for each list element
        input.append(0)
    
    # open code word file and read it
    try:
        fp = open(CodeFileName, 'r')
        # read file by 1 character as a binary number
        for i in range(0, q**m - 1):
            input[i] = int(fp.read(1), 2) # read data as a binary number
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(CodeFileName)
        sys.exit()

    # 1<= NumberOfErrors <= CorrectableBits
    NumberOfErrors = randint(1, CorrectableBits)
        
    # Decide Error Bits
    ErrorBits = []
    for i in range(0, NumberOfErrors):             
        ErrorBits.append(randint(0, CodeWordLength - 1))

    ErrorBits.sort()                   # sort the list
        
    #open file and write Error Bits
    # open file
    try:
        fp = open(INJECTFILE, 'w')
        #write user data to CHECKBITS
        for i in range(0, len(ErrorBits)):
            position = u"%d\n"%(ErrorBits[i])
            fp.write(position)    #write data as a character
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(INJECTFILE)
        sys.exit()        

    #reverse input list
    input.reverse()
    for i in ErrorBits:
        input[i] = bitflip(input[i])

    # reverse input for BMDecoder.py
    input.reverse()
    # open Errornous file and save data
    try:
        fp = open(ERRORFILE, 'w')
        #write user data to CHECKBITS
        for i in range(0, len(input)):
            fp.write(str(input[i]))    #write data as a character
        fp.close()
    except IOError:
        print "{0}を開けませんでした".format(INJECTFILE)
        sys.exit()        

if __name__ == '__main__':
    #translate command line argument
    argvs = sys.argv           #argvs is a list of commandline argument
    if len(argvs) != 2:
        print "Usage ./BCHEncoder560.py <FileName>"
        sys.exit()
    
    BaseElement = 2
    MultiplicativeOrder = 14
    CorrectableBits = 40
    if BaseElement == 2:
        NumberOfCheckBits = MultiplicativeOrder*CorrectableBits
    else:
        NumberOfCheckBits = 2*MultiplicativeOrder*CorrectableBits

    CodeFileName = argvs[1]
    dimension = BaseElement**MultiplicativeOrder - 1 - NumberOfCheckBits
    indata = generateData(dimension)
    encodeBCH560(indata, BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName)
    checkBCH560(BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName)
    injectErrors(BaseElement, MultiplicativeOrder, CorrectableBits, CodeFileName)
