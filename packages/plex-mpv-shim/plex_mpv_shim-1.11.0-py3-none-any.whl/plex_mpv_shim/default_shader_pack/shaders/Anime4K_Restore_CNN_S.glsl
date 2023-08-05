// MIT License

// Copyright (c) 2019-2021 bloc97
// All rights reserved.

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

//!DESC Anime4K-v4.0-Restore-CNN-(S)-Conv-4x3x3x3
//!HOOK MAIN
//!BIND MAIN
//!SAVE conv2d_tf
//!WIDTH MAIN.w
//!HEIGHT MAIN.h
//!COMPONENTS 4
#define go_0(x_off, y_off) (MAIN_texOff(vec2(x_off, y_off)))
vec4 hook() {
    vec4 result = mat4(-0.19288683, -0.21397883, 0.111997396, -0.04791413, -0.26682988, -0.06144587, -0.03601853, -0.16693151, 0.038494494, -0.16651472, 0.147657, -0.083003886, 0.0, 0.0, 0.0, 0.0) * go_0(-1.0, -1.0);
    result += mat4(-0.14286195, 0.08746566, -0.40107322, 0.12390977, -0.33392772, -0.18703035, -0.21326795, 0.04780781, -0.15155545, -0.0010025925, -0.1554875, -0.10676251, 0.0, 0.0, 0.0, 0.0) * go_0(-1.0, 0.0);
    result += mat4(0.28095165, 0.022872915, -0.21342312, -0.29982176, 0.025937587, -0.055012174, -0.33779636, 0.0015666655, 0.076416336, 0.06656033, -0.1557806, 0.1078894, 0.0, 0.0, 0.0, 0.0) * go_0(-1.0, 1.0);
    result += mat4(-0.31584853, 0.07527119, 0.30713862, -0.34014285, -0.50103146, -0.07217874, 0.512807, -0.09597398, -0.32097813, -0.051580857, -0.022466356, 0.01148551, 0.0, 0.0, 0.0, 0.0) * go_0(0.0, -1.0);
    result += mat4(-0.026032459, -0.04193211, 0.37703893, -0.031916667, -0.27421117, 1.0906446, -0.049654085, -0.19814016, 0.07819544, 0.06003738, 0.1405805, -0.0064135445, 0.0, 0.0, 0.0, 0.0) * go_0(0.0, 0.0);
    result += mat4(0.041450135, 0.11319654, -0.23237701, 0.08443178, 0.53344345, 0.30857387, -0.057264958, -0.1575803, 0.2325609, -0.027797326, -0.04544767, -0.18720597, 0.0, 0.0, 0.0, 0.0) * go_0(0.0, 1.0);
    result += mat4(0.2531829, -0.074966915, -0.27800754, -0.3146097, 0.20126024, -0.5380133, -0.15082566, -0.19021043, 0.29951036, 0.17123336, -0.01681872, -0.12574998, 0.0, 0.0, 0.0, 0.0) * go_0(1.0, -1.0);
    result += mat4(0.25203633, 0.19882993, 0.14906439, 0.13593598, 0.40712556, 0.084902965, 0.42969635, 0.2961132, -0.057267334, -0.030388135, 8.8084314e-05, 0.0210724, 0.0, 0.0, 0.0, 0.0) * go_0(1.0, 0.0);
    result += mat4(-0.13459359, -0.12199573, 0.12591946, 0.24736497, 0.2033463, -0.09388599, -0.094370656, 0.1071285, -0.18479438, -0.066625565, 0.08279283, 0.20130983, 0.0, 0.0, 0.0, 0.0) * go_0(1.0, 1.0);
    result += vec4(-0.011108127, -0.07481861, 0.07640154, 0.4964964);
    return result;
}
//!DESC Anime4K-v4.0-Restore-CNN-(S)-Conv-4x3x3x8
//!HOOK MAIN
//!BIND conv2d_tf
//!SAVE conv2d_1_tf
//!WIDTH conv2d_tf.w
//!HEIGHT conv2d_tf.h
//!COMPONENTS 4
#define go_0(x_off, y_off) (max((conv2d_tf_texOff(vec2(x_off, y_off))), 0.0))
#define go_1(x_off, y_off) (max(-(conv2d_tf_texOff(vec2(x_off, y_off))), 0.0))
vec4 hook() {
    vec4 result = mat4(-0.056432575, 0.0028165397, -0.026325442, -0.14802271, 0.16885762, -0.062179096, -0.2332292, 0.17513658, -0.08011296, 0.02947316, 0.014771492, -0.17946689, 0.026012989, -0.09823925, 0.036625937, -0.06924322) * go_0(-1.0, -1.0);
    result += mat4(-0.13571467, 0.09831142, 0.12911566, 0.06305893, -0.07188695, -0.20161287, 0.3858435, -0.21069056, -0.12294444, -0.1404628, -0.022659872, 0.23008968, 0.10969853, 0.17640765, 0.39796907, 0.20413099) * go_0(-1.0, 0.0);
    result += mat4(-0.0061665224, 0.055102807, -0.0059629944, -0.021429887, 0.061626043, 0.16898955, -0.21215646, 0.16510476, 0.2238265, 0.19429931, 0.09874656, 0.06828208, -0.122404456, -0.00026717107, -0.28203064, -0.29979932) * go_0(-1.0, 1.0);
    result += mat4(-0.22735378, 0.14538136, 0.11549746, 0.194148, -0.09841722, -0.0661309, 0.348576, -0.017375294, -0.044078812, 0.1298332, 0.04793373, -0.30687734, 0.08353025, 0.083519086, 0.10766399, 0.31796935) * go_0(0.0, -1.0);
    result += mat4(0.048365135, -0.17566709, -0.33212858, -0.052667376, -0.26443407, -0.010216014, 0.1573303, 0.05725314, 0.08140953, -0.09664591, 0.076109104, -0.026773714, 0.07732627, 0.10188082, -0.28266954, -0.16230233) * go_0(0.0, 0.0);
    result += mat4(0.29931107, 0.117944, -0.10414009, 0.12795551, 0.12576093, 0.17082554, -0.15803693, 0.13430743, -0.025801308, -0.10797019, 0.0721032, 0.2825884, -0.11025257, 0.12798019, 0.081827976, -0.050441865) * go_0(0.0, 1.0);
    result += mat4(-0.11827391, 0.08306765, -0.3430314, 0.07898041, -0.023839617, -0.019507334, 0.23176382, -0.40992323, 0.09411734, 0.38415068, -0.25845516, -0.29984522, 0.1470966, -0.0684779, -0.07071314, -0.026773235) * go_0(1.0, -1.0);
    result += mat4(0.19091596, 0.082110435, -0.5266589, -0.1744098, -0.015838385, -0.046316292, 0.023171103, -0.03731331, 0.2642396, 0.31824252, -0.041754793, -0.09525519, -0.14696182, 0.052168854, 0.039857205, -0.027555354) * go_0(1.0, 0.0);
    result += mat4(0.15207373, 0.09845733, 0.0142631065, 0.096375965, 0.06089903, 0.17902578, -0.42391995, 0.22475442, 0.016356342, -0.06277531, -0.12173141, -0.18635495, -0.0013459618, 0.15725887, 0.019310836, 0.20293565) * go_0(1.0, 1.0);
    result += mat4(-0.18395247, 0.30672902, 0.09034339, 0.1821889, -0.0419004, -0.2169228, -0.14052129, 0.11006559, 0.1709272, 0.51062274, 0.13758625, -0.2242552, -0.030382963, 0.3357568, -0.26491287, 0.02501938) * go_1(-1.0, -1.0);
    result += mat4(0.040511727, 0.12523083, -0.27318433, 0.08388512, 0.25354835, 0.3404216, -0.2632471, -0.17784123, 0.2732347, 0.4468553, 0.084667034, -0.1856242, 0.034099877, -0.00954992, -0.32751867, -0.062207516) * go_1(-1.0, 0.0);
    result += mat4(0.17564747, 0.11645554, -0.16362113, 0.105654195, -0.2762563, -0.1413764, 0.23264363, -0.14000498, 0.095402054, 0.0715738, -0.19346157, -0.028285999, 0.009799127, 0.04059529, 0.19688335, 0.1282381) * go_1(-1.0, 1.0);
    result += mat4(0.23575781, -0.11446148, -0.20504695, 0.035568226, 0.36890212, -0.85968876, -0.18545328, 0.33796397, -0.30916876, -0.10445518, -0.3046253, 0.33271998, -0.06263589, -0.2160114, -0.16383372, -0.31173357) * go_1(0.0, -1.0);
    result += mat4(0.20469664, 0.4039374, -0.070057206, 0.030353077, 0.39843914, -0.15490077, -0.24476516, 0.38238233, -0.21809858, 0.23496576, -0.051794037, 0.033664484, -0.14411364, -0.2515329, 0.124655396, -0.05818785) * go_1(0.0, 0.0);
    result += mat4(-0.09065731, -0.16787091, 0.013269188, 0.23687351, -0.41504318, -0.048163068, 0.31760025, -0.33648986, 0.29752317, 0.2926866, 0.14408836, -0.33382463, -0.15873958, -0.121961035, 0.11797893, 0.09000567) * go_1(0.0, 1.0);
    result += mat4(0.13356976, 0.013763947, 0.012169505, -0.109594524, 0.03417223, 0.7031121, 0.65146804, 0.5250268, -0.50132495, -0.419648, 0.2940041, 0.83051753, -0.17595838, 0.1633008, -0.018587278, 0.079596795) * go_1(1.0, -1.0);
    result += mat4(0.07570128, -0.1581438, 0.03904949, 0.14890033, -0.054611947, 0.17469402, -0.44252598, 0.036181703, -0.4981031, -0.37507218, -0.18466389, 0.2645845, 0.25189674, -0.025896115, 0.034307647, -0.020462232) * go_1(1.0, 0.0);
    result += mat4(-0.11645865, 0.02296537, 0.040909223, 0.015069485, 0.062284566, -0.22526766, 0.09241534, -0.32623053, 0.18208642, 0.3954284, 0.2884468, -0.25137675, -0.037232924, -0.10185309, -0.17956531, 0.018966453) * go_1(1.0, 1.0);
    result += vec4(-0.16371979, -0.024620198, -0.035754893, 0.04176776);
    return result;
}
//!DESC Anime4K-v4.0-Restore-CNN-(S)-Conv-4x3x3x8
//!HOOK MAIN
//!BIND conv2d_1_tf
//!SAVE conv2d_2_tf
//!WIDTH conv2d_1_tf.w
//!HEIGHT conv2d_1_tf.h
//!COMPONENTS 4
#define go_0(x_off, y_off) (max((conv2d_1_tf_texOff(vec2(x_off, y_off))), 0.0))
#define go_1(x_off, y_off) (max(-(conv2d_1_tf_texOff(vec2(x_off, y_off))), 0.0))
vec4 hook() {
    vec4 result = mat4(0.01921286, -0.26684764, -0.12663573, 0.31641877, -0.25313398, 0.12264074, 0.58750325, -0.14084283, 0.5837018, -0.042300556, -0.20435576, -0.009954825, 0.060783498, 0.05540401, 0.2205112, -0.06578902) * go_0(-1.0, -1.0);
    result += mat4(-0.21930243, -0.03774968, 0.22615197, 0.18338196, 0.011201461, -0.271034, 0.00573116, -0.12248194, 0.47990513, 0.2982416, -0.1087603, -0.050099242, -0.07620939, -0.07148229, 0.03691984, -0.16796488) * go_0(-1.0, 0.0);
    result += mat4(-0.14962853, -0.053769328, 0.02387081, 0.22002189, 0.052237745, -0.26160842, -0.08603077, 0.012542448, 0.08119985, 0.075785555, -0.33437458, -0.43373227, -0.13206963, -0.08759176, -0.03288923, -0.09799959) * go_0(-1.0, 1.0);
    result += mat4(-0.1305593, -0.5974288, 0.06058367, 0.08406488, 0.013692483, 0.06646377, 0.16469325, 0.08990975, 0.42217395, -0.11289523, -0.06165009, 0.48556912, -0.15702641, -0.19922857, -0.0035429662, -0.0022089656) * go_0(0.0, -1.0);
    result += mat4(-0.1964807, 0.038099788, 0.21587034, 0.039734077, -0.07063389, 0.11604167, -0.24558097, -0.08900199, -0.7684516, -0.1037487, -0.09380674, 0.33144563, -0.16653742, 0.0028585843, -0.33774406, -0.0528696) * go_0(0.0, 0.0);
    result += mat4(-0.27298656, -0.05665099, 0.09661685, 0.19780266, 0.1025106, -0.22055034, -0.21218458, -0.040628925, 0.0095010325, 0.13118382, -0.42582452, -0.22197723, 0.21006055, -0.06189587, -0.15285942, -0.09526762) * go_0(0.0, 1.0);
    result += mat4(-0.14494462, -0.046788953, 0.065877035, 0.09911713, 0.35096622, 0.16682479, 0.028363144, 0.36037162, 0.29413632, 0.28212717, -0.025364442, -0.3406269, 0.047262143, -0.11892685, -0.008032766, 0.29743317) * go_0(1.0, -1.0);
    result += mat4(-0.15191558, -0.36980554, 0.14555687, 0.0043930537, -0.012661432, 0.15737776, -0.115250416, 0.10324491, 0.24491951, -0.15575431, -0.27802598, 0.21959937, 0.18063772, 0.4455559, -0.09693302, 0.33382267) * go_0(1.0, 0.0);
    result += mat4(0.2717801, 0.13452889, 0.14105384, 0.16324317, -0.40111846, 0.1154301, -0.0076733204, -0.09697362, 0.44306824, -0.02831414, -0.2153124, -0.12075326, 0.060776163, 0.30347148, -0.0036976219, -0.12070682) * go_0(1.0, 1.0);
    result += mat4(-0.39780128, -0.29875937, -0.12952097, 0.080333896, 0.07520163, 0.021689568, -0.23121156, -0.038140096, -0.1593877, 0.017156163, -0.06038025, 0.009244022, -0.13917233, 0.30957314, 0.243109, -0.104947075) * go_1(-1.0, -1.0);
    result += mat4(-0.07965157, 0.06776501, -0.13288979, 0.005851189, -0.08768168, -0.03689969, 0.12034646, 0.22441491, 0.14453568, -0.17648841, -0.3378289, -0.018329712, 0.11722939, -0.34161824, 0.08424494, -0.01400687) * go_1(-1.0, 0.0);
    result += mat4(0.08153887, 0.07222914, -0.14663404, -0.038526025, -0.07385973, 0.18440577, 0.35890242, 0.17084727, 0.26345527, 0.15280858, -0.007446105, -0.024403179, -0.30336383, -0.22978698, 0.11612946, -0.23614909) * go_1(-1.0, 1.0);
    result += mat4(-0.07447396, 0.09023449, -0.13798, -0.086943336, -0.30787337, 0.15087669, 0.14418626, -0.03371195, 0.048989657, -0.13075387, -0.13458036, -0.059836224, 0.06495196, 0.269715, 0.3674355, 0.38956037) * go_1(0.0, -1.0);
    result += mat4(0.34981915, -0.048779126, 0.31717536, 0.38080826, -0.20149232, -0.82969636, -0.10167862, 0.6382858, 0.25976858, 0.4370118, -0.04724865, -0.10014156, 0.19380626, -0.080370255, 0.09578106, -0.035166856) * go_1(0.0, 0.0);
    result += mat4(-0.026443917, 0.4132611, 0.01822534, 0.12742202, -0.26652107, -0.2996705, 0.30905882, 0.07989903, 0.38249823, 0.21486135, 0.025314959, -0.14717339, -0.13344015, -0.32088286, -0.2833883, -0.30973712) * go_1(0.0, 1.0);
    result += mat4(0.021517841, 0.006556378, 0.2025686, -0.12044382, -0.38583103, -0.0027515136, -0.06556736, -0.097090125, 0.04676486, -0.11954886, -0.051612873, 0.07831412, -0.18823163, -0.16542958, 0.04245155, 0.6437998) * go_1(1.0, -1.0);
    result += mat4(-0.39475346, -0.2936861, 0.26768062, -0.28151843, 0.21935691, 0.2101108, -0.15455097, 0.19548604, 0.09188909, -0.020147726, 0.103328265, -0.12574542, -0.34167948, 0.07523185, -0.17669058, 0.62446547) * go_1(1.0, 0.0);
    result += mat4(-0.37661025, -0.29630858, 0.05451026, 0.1611643, 0.14079669, -0.2170294, -0.038716137, 0.13514164, -0.21235192, -0.07860726, -0.005749412, 0.025625167, -0.13297133, 0.33012658, -0.27434957, -0.18416783) * go_1(1.0, 1.0);
    result += vec4(-0.0036821906, -0.050239526, -0.01355402, 0.00048220603);
    return result;
}
//!DESC Anime4K-v4.0-Restore-CNN-(S)-Conv-3x3x3x8
//!HOOK MAIN
//!BIND MAIN
//!BIND conv2d_2_tf
//!SAVE MAIN
//!WIDTH conv2d_2_tf.w
//!HEIGHT conv2d_2_tf.h
#define go_0(x_off, y_off) (max((conv2d_2_tf_texOff(vec2(x_off, y_off))), 0.0))
#define go_1(x_off, y_off) (max(-(conv2d_2_tf_texOff(vec2(x_off, y_off))), 0.0))
vec4 hook() {
    vec4 result = mat4(0.15873, 0.17989138, 0.14648493, 0.0, -0.017379675, -0.017363746, -0.019855022, 0.0, 0.009670625, 0.0070157526, 0.0075994316, 0.0, 0.025388412, 0.027231036, 0.024052646, 0.0) * go_0(-1.0, -1.0);
    result += mat4(0.048195973, 0.041760173, 0.037366055, 0.0, -0.115950756, -0.12887983, -0.12535639, 0.0, 0.032125086, 0.03397254, 0.032950625, 0.0, 0.01223746, 0.020822672, 0.0161561, 0.0) * go_0(-1.0, 0.0);
    result += mat4(0.0890567, 0.094453335, 0.09014035, 0.0, 0.016081346, 0.017434116, 0.020783134, 0.0, -0.011775135, -0.010094134, -0.018522855, 0.0, 0.072103254, 0.07940666, 0.065876864, 0.0) * go_0(-1.0, 1.0);
    result += mat4(-0.04841196, -0.06963968, -0.056574684, 0.0, 0.10912542, 0.11813441, 0.10643838, 0.0, -0.013013885, -0.01562045, -0.013802797, 0.0, 0.037505716, 0.04352026, 0.04645123, 0.0) * go_0(0.0, -1.0);
    result += mat4(-0.3472869, -0.36243078, -0.33530185, 0.0, 0.23654196, 0.2305048, 0.22150646, 0.0, -0.045226905, -0.041799217, -0.042511635, 0.0, -0.10267792, -0.1123385, -0.10845448, 0.0) * go_0(0.0, 0.0);
    result += mat4(0.011987401, 0.012285043, 0.007813165, 0.0, -0.15911353, -0.17523928, -0.1535267, 0.0, 0.15675929, 0.16531634, 0.15948962, 0.0, -0.09240023, -0.09513292, -0.084187366, 0.0) * go_0(0.0, 1.0);
    result += mat4(0.069052905, 0.07278333, 0.0756627, 0.0, -0.012180326, -0.018794727, -0.031050753, 0.0, -0.044663202, -0.04362803, -0.038904265, 0.0, -0.008540197, -0.011201734, -0.01556625, 0.0) * go_0(1.0, -1.0);
    result += mat4(-0.08261173, -0.09042543, -0.07589266, 0.0, 0.043515377, 0.045066774, 0.04037769, 0.0, -0.06262993, -0.07469342, -0.058593787, 0.0, 0.026696987, 0.028740842, 0.037405368, 0.0) * go_0(1.0, 0.0);
    result += mat4(0.07975598, 0.09597654, 0.08997132, 0.0, -0.07844719, -0.07880916, -0.06835411, 0.0, 0.05668995, 0.050163813, 0.053357534, 0.0, -0.020040333, -0.019867316, -0.01907621, 0.0) * go_0(1.0, 1.0);
    result += mat4(-0.017078733, -0.017393313, -0.008266595, 0.0, -0.0033478448, -0.0027439648, -0.0042334674, 0.0, -0.06354017, -0.062058125, -0.04652064, 0.0, -0.010787706, -0.0062706997, -0.007573461, 0.0) * go_1(-1.0, -1.0);
    result += mat4(-0.019895451, -0.016341688, -0.008712399, 0.0, 0.026231976, 0.023955572, 0.0216376, 0.0, -0.061950512, -0.05481285, -0.05261985, 0.0, -0.018804235, -0.016235247, -0.0131616965, 0.0) * go_1(-1.0, 0.0);
    result += mat4(-0.055628926, -0.063315354, -0.057192408, 0.0, -0.0256364, -0.028660972, -0.02937357, 0.0, -0.017604912, -0.020851422, -0.016070362, 0.0, -0.0870202, -0.0832279, -0.07525406, 0.0) * go_1(-1.0, 1.0);
    result += mat4(0.062738225, 0.07106593, 0.061644047, 0.0, -0.06068257, -0.06983662, -0.066070385, 0.0, 0.024919355, 0.03227179, 0.028569462, 0.0, -0.07866227, -0.098967604, -0.092128105, 0.0) * go_1(0.0, -1.0);
    result += mat4(0.040397774, 0.047241107, 0.03962998, 0.0, -0.09112752, -0.10057507, -0.09301817, 0.0, 0.10833967, 0.101835825, 0.10027467, 0.0, 0.27189335, 0.27433604, 0.26781923, 0.0) * go_1(0.0, 0.0);
    result += mat4(-0.044211388, -0.042373534, -0.03658007, 0.0, 0.113148406, 0.12423258, 0.107804194, 0.0, -0.17081551, -0.18562958, -0.17475435, 0.0, 0.09636739, 0.10763415, 0.093332425, 0.0) * go_1(0.0, 1.0);
    result += mat4(-0.03798545, -0.047811143, -0.050768293, 0.0, 0.018775463, 0.026812987, 0.03452908, 0.0, 0.0055677597, 0.0039081173, -0.0017878668, 0.0, -0.10728597, -0.12618187, -0.109045394, 0.0) * go_1(1.0, -1.0);
    result += mat4(0.06359783, 0.064184755, 0.04934199, 0.0, -0.009819327, -0.006616115, -0.007431496, 0.0, 0.025055679, 0.024787048, 0.017360551, 0.0, -0.047140837, -0.061695747, -0.06440822, 0.0) * go_1(1.0, 0.0);
    result += mat4(0.060199022, 0.06482763, 0.059514645, 0.0, 0.026998974, 0.028776823, 0.024897143, 0.0, 0.17968474, 0.19337215, 0.16760105, 0.0, 0.0075838566, 0.010503482, 0.011993149, 0.0) * go_1(1.0, 1.0);
    result += vec4(-0.0052927984, -0.0060193934, -0.0048643993, 0.0);
    return result + MAIN_tex(MAIN_pos);
}
