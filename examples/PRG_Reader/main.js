//GLOBALs
//the file data and the patch command data
var fileData, patchData;

//pointer into the byte array. Used throughout the following.
//Always points to the next unread byte
var ptr=0;
var ptr0=0;//used to record the pointer at the start of the actual patch

//used to accumulate the hex representation of the MIDI data (i.e. the actual patch data)
var patchHex;

var voiceMode="";//values from voiceValues

//the patch name
var patchName="";

//Look-up lists for the encoded settings
var voiceValues = ["Single","Undefined","Layer","Vocoder"];
var timebaseValues = ["1/32","1/24","1/16","1/12","3/32","1/8","1/6","3/16","1/4",
"1/3","3/8","1/2","2/3","3/4","1/1"];//used for delay, see "T-1" in MIDI implementation gudie
var delayTypes=["Stero","Cross","L-R"];
var modfxTypes=["Cho/flg","Ensemble","Phaser"];
var hiF=["1kHz","1.25kHz","1.5kHz","1.75kHz","2kHz","2.25kHz","2.5kHz","2.75kHz","3kHz",
"3.25kHz","3.5kHz","3.75kHz","4kHz","4.25kHz","4.5kHz","4.75kHz","5kHz","5.25kHz","5.5kHz",
"5.75kHz","6kHz","7kHz","8kHz","9kHz","10kHz","11kHz","12kHz","14kHz","16kHz","18kHz"];
var loF=["40Hz","50Hz","60Hz","80Hz","100Hz","120Hz","140Hz","160Hz","180Hz","200Hz",
"220Hz","240Hz","260Hz","280Hz","300Hz","320Hz","340Hz","360Hz","380Hz","400Hz","420Hz",
"440Hz","460Hz","480Hz","500Hz","600Hz","700Hz","800Hz","900Hz","1000Hz"];
var arpTargetTimbre=["Both","Timbre1","Timbre2"];
var arpTypes=["Up","Down","Alt1","Alt2","Random","Trigger"];
var arpResolution=["1/24","1/16","1/12","1/8","1/6","1/4"];
var voiceModeTypes=["Mono","Poly","Unison"];
var triggerMode=["Single","Multi"];
var osc1Waves=["Saw","Square","Triangle","Sine","Vox Wave","DWGS","Noise","Audio In"];
var osc2Mod=["None","Sync","Ring","Ring-Sync"];
var osc2Waves=["Saw","Square","Triangle"];
var filterType=["-24dB LP","-12dB LP", "-12dB BP", "-12dB HP"];
var lfoSync=["Off","Timbre","Voice"];
var lfo1Waves=["Saw","Square","Triangle","S&H"];
var lfo2Waves=["Saw","Squ+","Sine","S&H"];
var lfoSyncNote=["1/1","3/4","2/3","1/2","3/8","1/3","1/4","3/16","1/6","1/8",
"3/32","1/12","1/16","1/24","1/32"];
var patchSource=["EG1","EG2","LFO1","LFO2","Velocity","Key Track","Bend","Mod Wheel"];
var patchDestination=["Pitch","Osc2 Pitch","Ctl1","Noise","Cutoff","Amp","Pan","LFO2 Freq"];
var formantShift=["0","+1","+2","-1","-2"];
var fcmodSource=["---","Amp EG","LFO 1","LFO 2","Velocity","Key Track","Bend", "Mod Wheel"];


//this holds the patch as an edit-section, knob matrix.
//it is sectioned because the settings of VOICE determine what is needed
var arpa=0, arpb=1, pattern=2,state=3;
var arpLabels = ["Areggio A","Arpeggio B","Arp. Pattern","Arp. State"];
var arp;

var delay=1, modfx=0, eq=2;
var fx
var fxLabels = ["Mod FX","Delay","EQ"];

var voice=0, pitch=1, osc1=2, osc2=3, mix=4, filter=5, fEG=6, amp=7, aEG=8, lfo1=9,
lfo2=10, patch1=11, patch2=12, patch3=13, patch4=14;//array indices
var timbre1;
var timbre2;
var audio1=3, fcmod=6, chleva =11, chlevb=12, chpana=13, chpanb=14 //array indices, voice,pitch, osc1, mix, filter, amp, ampeg, lfo1, lfo2 shared with timbres
var vocoder;

var timbreLabels=["Voice","Pitch","Osc 1","Osc 2","Mix Levels","Filter","Filter EG","Amp",
"Amp EG","LFO 1","LFO 2","Patch 1","Patch 2","Patch 3","Patch 4"];
var vocoderLabels=["Voice","Pitch","Osc 1","Audio In 1","Mix Levels","Filter","Cutoff Mod","Amp",
"Amp EG","LFO 1","LFO 2","Ch Levels A","Ch Levels B","Ch Pan A","Ch Pan B"];


function processData(fileBuffer){
//get the data into a real array, as pure bytes
fileData = new Uint8Array(fileBuffer);

//find the start of the SysEx
for(var i=0;i<fileData.length;i++){
	if(fileData[i]==0xF0){
		ptr=i+1;
		break;
	}
}

//clear messages (in case previously set)
document.getElementById("messages").innerHTML="";

//did we fail to find a SysEx?
if(ptr==0){
document.getElementById("messages").innerHTML="Failed to find start of SysEx. Not a valid .prg file.";
return;
}

//ptr is currently at the start of the length info
//length is a "variable length quantity", in which the last byte is 
//indicated by bit7=0, while preceeding bytes have bit7=1
// at the end of this, bytes2read = the length of the patch + 4
var bytes2read = fileData[ptr]&0x7F;
do{
	ptr++;
	var bitshift = bytes2read&0x01;
	bytes2read = (bytes2read >> 1)*256 + bitshift*128 + (fileData[ptr]&0x7F);
}while(fileData[ptr]&0x80);
//position to byte after length
ptr++;

//check that the manufacturer and device are for microKorg
//the midi channel is at ptr+1, and is ignored
if(!(fileData[ptr]==0x42 && fileData[ptr+2]==0x58)){
	document.getElementById("messages").innerHTML="File is not from a microKorg or is not a single patch (could be a full dump)";
	return;
}
ptr+=3;

//this byte should be 0x40 if the data is a "current program data dump"
if(fileData[ptr]!=0x40){
	document.getElementById("messages").innerHTML="The file appears not to be a single patch program (was expecting byte 0x40 to signal &quot;current program data dump&quot; but found "+fileData[ptr].toString(16);
	return;
}
ptr++;

//this is the start point as far as patch data
ptr0=ptr;

//reset the raw-ish hex string.
//This will be built up during read8to7() calls
patchHex="Patch Hex=\r\n";

//7 bytes of patch data is stored in 8 byte chunks
//read all the patch data into patchData[]
var chunks2read = Math.floor((bytes2read-4)/8);
var patchByte=0;
patchData=new Uint8Array(chunks2read*7);
for(var i=0;i<chunks2read;i++){
	var chunk = read8to7(fileData);
	for(var j=0;j<7;j++){
		patchData[patchByte] = chunk[j];
		patchByte++;
	}
}

//The F7 terminator should appear
ptr+=bytes2read - chunks2read*8-5;
if(fileData[ptr]!=0xF7){
	document.getElementById("messages").innerHTML="Failed to detect correct (0xF7) ending byte. Continuing to process, but assume an error in the data.";
}

// ---------------- patchData is ready to be converted to human-accessible form
//reset the patch data arrays
arp = [["--","--","--","--","--"],["--","--","--","--","--"],["--"],["--"]];
fx = [["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"]];
timbre1=[["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"]];
timbre2=[["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"]];
vocoder=[["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"],["--","--","--","--","--"],["--","--","--","--","--"],
["--","--","--","--","--"]];

//patch data in common to all voiceModes (single/layer/vocoder)
doArpeggiatorAndEffects();

//Depending on the voiceMode, decode different parts of patchData.
//Note that patchData contains blocks for timbre1, timbre2 and vocoder,
//irrespective of the mode.
// while we are at it, hack-in the voice mode setting,
//which don't quite match the user's patch settings
if(voiceMode=="Vocoder"){
    vocoder[voice][0]="Vocoder";
    doVocoder();
}else{
    timbre1[voice][0]="Synth";
    timbre1[voice][1]=voiceMode;
    doTimbre(timbre1, 38);//timbre1 starts at patch byte 38
    if(voiceMode=="Layer"){
        timbre2[voice][0]="Synth";
        timbre2[voice][1]=voiceMode;
        doTimbre(timbre2, 146);//timbre1 starts at patch byte 146
    }
}


// prepare the human-readable patch text and output

var patchText=patchName+"\r\n";
//
if(voiceMode=="Single" || voiceMode=="Layer"){
	if(voiceMode=="Layer"){
		patchText+="[[TIMBRE 1]]\r\n";
	}
	for(var i=0;i<15;i++){
		patchText+="["+timbreLabels[i]+"]: ";
		patchText+=formatText(timbre1[i]);
	}
	if(voiceMode=="Layer"){
		patchText+="[[TIMBRE 2]]\r\n";
		for(var i=0;i<15;i++){
			patchText+="["+timbreLabels[i]+"]: ";
			patchText+=formatText(timbre2[i]);
		}
	}	

}else if(voiceMode="Vocoder"){
		for(var i=0;i<15;i++){
			patchText+="["+vocoderLabels[i]+"]: ";
			patchText+=formatText(vocoder[i]);
		}
	//document.getElementById("messages").innerHTML="Vocoder Patch - not currently supported";
}
//Output stages: fx,delay, eq
for(var i=0;i<3;i++){
	patchText+="["+fxLabels[i]+"]: ";
	patchText+=formatText(fx[i]);
}
//arpeggiator
for(var i=0;i<4;i++){
	patchText+="["+arpLabels[i]+"]: ";
	patchText+=formatText(arp[i]);
}

document.getElementById("hex").innerHTML = patchHex;
document.getElementById("patch").innerHTML = patchText;
}


//read patch bytes 0 to 37, which covers the name, apreggiator settings, effects settings (incl EQ), and the "voiceMode", which indicates the patch type (single, layered, vocoder)
function doArpeggiatorAndEffects(){
    patchName="";
    for(var i=0;i<12;i++){
        patchName+=String.fromCharCode(patchData[i]);
    }
    patchName = patchName.trim();
    //2 dummy bytes - skipped

    //14
    arp[arpb][3]=(patchData[14]&0x07)+1;
    //15
    var p="";
    var thisByte=patchData[15];
    for(var i=0;i<8;i++){
        p+=thisByte&0x01?"no":"yes";
        if(i<7) p+=",";
        thisByte=thisByte>>1;
    }
    arp[pattern][0]=p;
    //16
    var bits=(patchData[16] >>4)&0x03;
    voiceMode = voiceValues[bits];
    //17,18 not used
    //19
    bits=patchData[19]&0x80;
    fx[delay][1]=bits?"on":"off";
    if(bits){
        //delay is a timebase only if tempo sync is on
        fx[delay][2]=timebaseValues[patchData[19]&0x0F];
    }else{
        //20 (otherwise use the time value)
        fx[delay][2] = patchData[20];
    }
    //21
    fx[delay][3]=patchData[21];
    //22
    fx[delay][0]=delayTypes[patchData[22]];
    //23
    fx[modfx][1]=patchData[23];
    //24
    fx[modfx][2]=patchData[24];
    //25
    fx[modfx][0]=modfxTypes[patchData[25]];
    //26
    fx[eq][2]=hiF[patchData[26]];
    //27
    fx[eq][3]=reRange(patchData[27],12);
    //28
    fx[eq][0]=loF[patchData[28]];
    //29
    fx[eq][1]=reRange(patchData[29],12);
    //30 and 31 = arp tempo (MSB, LSB)
    arp[arpa][0]=patchData[30]*256+patchData[31];
    //32
    arp[state][0]=(patchData[32]&0x80)?"on":"off";
    arp[arpb][0]=(patchData[32]&0x40)?"on":"off";
    arp[arpb][4]=arpTargetTimbre[(patchData[32]>>4)&0x03];
    arp[arpb][2]=(patchData[32]&0x01)?"on":"off";
    //33
    arp[arpa][3]=arpTypes[patchData[33]&0x0F];
    arp[arpa][4]=1+(patchData[33]>>4)&0x03;
    //34
    arp[arpa][2]=Math.max(patchData[34],100)+"%";
    //35
    arp[arpa][1]=arpResolution[patchData[35]];
    //36
    thisByte=patchData[36];
    if(thisByte>100){
        thisByte=thisByte-256;
    }
    arp[arpb][1]=thisByte;
    //37 
    // - octave shift setting - skip
}


//Both timbres are identical in form, but start at different bytes.
//the 1st arg will receive either of timbre1 or timbre2 variables, which
// will be populated in this function because objects are passed by reference
function doTimbre(timbre, startAt){
	//0
	// - MIDI channel - skip
	//1
	bits=(patchData[startAt+1]>>6)&0x03;
	timbre[voice][2]=voiceModeTypes[bits];
	timbre[aEG][4]=(patchData[startAt+1]&0x20)?"yes":"no";
	timbre[fEG][4]=(patchData[startAt+1]&0x10)?"yes":"no";
	if(bits!=1){
		timbre[voice][3]=triggerMode[(patchData[startAt+1]>>3)&0x01];
	}
	//2 - detune only applicable if unison
	if(bits==2){
		timbre[voice][4]=patchData[startAt+2];
	}
	//3
	timbre[pitch][1]=reRange(patchData[startAt+3],+50);
	//4
	timbre[pitch][3]=reRange(patchData[startAt+4],12);
	//5
	timbre[pitch][0]=reRange(patchData[startAt+5],24);
	//6
	timbre[pitch][4]=patchData[startAt+6]-64;
	//7
	bits =patchData[startAt+7]&0x07;
	timbre[osc1][0]=osc1Waves[bits];
	//8
	timbre[osc1][1]=patchData[startAt+8];
	//9
	timbre[osc1][2]=patchData[startAt+9];
	//10 - only for DWGS type (overwrites ctrl 2)
	if(bits==5){
		timbre[osc1][2]=patchData[startAt+10];
	}
	//11 -dummy byte
	//12
	timbre[osc2][0]=osc2Waves[patchData[startAt+12]&0x03];
	timbre[osc2][1]=osc2Mod[(patchData[startAt+12]>>4)&0x03];
	//13
	timbre[osc2][2]=reRange(patchData[startAt+13],24);
	//14
	timbre[osc2][3]=patchData[startAt+14]-64;
	//15
	timbre[pitch][2]=patchData[startAt+15];
	//16
	timbre[mix][0]=patchData[startAt+16];
	//17
	timbre[mix][1]=patchData[startAt+17];
	//18
	timbre[mix][2]=patchData[startAt+18];
	//19
	timbre[filter][0] = filterType[patchData[startAt+19]];
	//20
	timbre[filter][1]=patchData[startAt+20];
	//21
	timbre[filter][2]=patchData[startAt+21];
	//22
	timbre[filter][3]=patchData[startAt+22]-64;
	//23 - not used 
	//24
	timbre[filter][4]=patchData[startAt+24]-64;
	//25
	timbre[amp][0]=patchData[startAt+25];
	//26
	timbre[amp][1]=panText(patchData[startAt+26]);
	//27
	timbre[amp][2]=patchData[startAt+27]&0x01?"on":"off";
	//28
	// - velocity sense not used
	//29
	timbre[amp][3]=patchData[startAt+29]-64;
	//30
	timbre[fEG][0]=patchData[startAt+30];
	//31
	timbre[fEG][1]=patchData[startAt+31];
	//32
	timbre[fEG][2]=patchData[startAt+32];
	//33
	timbre[fEG][3]=patchData[startAt+33];
	//34
	timbre[aEG][0]=patchData[startAt+34];
	//35
	timbre[aEG][1]=patchData[startAt+35];
	//36
	timbre[aEG][2]=patchData[startAt+36];
	//37
	timbre[aEG][3]=patchData[startAt+37];
	//38
	timbre[lfo1][0]=lfo1Waves[patchData[startAt+38]&0x03];
	timbre[lfo1][1]=lfoSync[(patchData[startAt+38]>>4)&0x03];
	//39
	timbre[lfo1][3]=patchData[startAt+39];
	//40
	timbre[lfo1][2]=patchData[startAt+40]&0x80?"on":"off";
	if(patchData[startAt+40]&0x80){
		//temp sync=on will over-write LFO freq with sync note
		timbre[lfo1][3]=lfoSyncNote[patchData[startAt+40]&0x0F];
	}
	//41
	timbre[lfo2][0]=lfo2Waves[patchData[startAt+41]&0x03];
	timbre[lfo2][1]=lfoSync[(patchData[startAt+41]>>4)&0x03];
	//42
	timbre[lfo2][3]=patchData[startAt+42];
	//43
	timbre[lfo2][2]=patchData[startAt+43]&0x80?"on":"off";
	if(patchData[startAt+43]&0x80){
		//temp sync=on will over-write LFO freq with sync note
		timbre[lfo2][3]=lfoSyncNote[patchData[startAt+43]&0x0F];
	}
	//44
	timbre[patch1][0]=patchSource[patchData[startAt+44]&0x0F];
	timbre[patch1][1]=patchDestination[(patchData[startAt+44]>>4)&0x0F];
	//45
	timbre[patch1][2]=patchData[startAt+45]-64;
	//46
	timbre[patch2][0]=patchSource[patchData[startAt+46]&0x0F];
	timbre[patch2][1]=patchDestination[(patchData[startAt+46]>>4)&0x0F];
	//47
	timbre[patch2][2]=patchData[startAt+47]-64;
	//48
	timbre[patch3][0]=patchSource[patchData[startAt+48]&0x0F];
	timbre[patch3][1]=patchDestination[(patchData[startAt+48]>>4)&0x0F];
	//49
	timbre[patch3][2]=patchData[startAt+49]-64;
	//50
	timbre[patch4][0]=patchSource[patchData[startAt+50]&0x0F];
	timbre[patch4][1]=patchDestination[(patchData[startAt+50]>>4)&0x0F];
	//51
	timbre[patch4][2]=patchData[startAt+51]-64;

	//THERE ARE dummy bytes from 52-107)
}

//quite a few sections are identical to doTimbre, but there are some small diffs
// AND the sections often appear at different byte positions. so code is duplicated
function doVocoder(){
	startAt=38;
	//0
	// - MIDI channel - skip
	//1
	var bits=(patchData[startAt+1]>>6)&0x03;
	vocoder[voice][2]=voiceModeTypes[bits];
	vocoder[aEG][4]=(patchData[startAt+1]&0x20)?"yes":"no";
	if(bits!=1){
		vocoder[voice][3]=triggerMode[(patchData[startAt+1]>>3)&0x01];
	}
	//2 - detune only applicable if unison
	if(bits==2){
		vocoder[voice][4]=patchData[startAt+2];
	}
	//3
	vocoder[pitch][1]=reRange(patchData[startAt+3],+50);
	//4
	vocoder[pitch][3]=reRange(patchData[startAt+4],12);
	//5
	vocoder[pitch][0]=reRange(patchData[startAt+5],24);
	//6
	vocoder[pitch][4]=patchData[startAt+6]-64;
	//7
	bits =patchData[startAt+7]&0x07;
	vocoder[osc1][0]=osc1Waves[bits];
	//8
	vocoder[osc1][1]=patchData[startAt+8];
	//9
	vocoder[osc1][2]=patchData[startAt+9];
	//10 - only for DWGS type (overwrites ctrl 2)
	if(bits==5){
		vocoder[osc1][2]=patchData[startAt+10];
	}
	//11 -dummy byte
	//12
	vocoder[audio1][3]=(patchData[startAt+9]&0x01)?"enabled":"disabled";
	//13
	// - dummy
	//14
	vocoder[pitch][2]=patchData[startAt+14]&0x7F;

	//15
	vocoder[mix][0]=patchData[startAt+15];	
	//16
	vocoder[mix][1]=patchData[startAt+16];
	//17
	vocoder[mix][2]=patchData[startAt+17];
	//18
	vocoder[audio1][2]=patchData[startAt+18];
	//19
	vocoder[audio1][0]=patchData[startAt+19];
	//20
	vocoder[audio1][1]=patchData[startAt+20];
	//21
	vocoder[filter][0]=formantShift[patchData[startAt+21]];
	//22
	vocoder[filter][1]=patchData[startAt+22]-64;
	//23
	vocoder[filter][2]=patchData[startAt+23];
	//24
	vocoder[fcmod][0]=fcmodSource[patchData[startAt+24]];
	//25
	vocoder[fcmod][1]=patchData[startAt+25]-64;
	//26
	var tmp=patchData[startAt+26];
	if(tmp == 127){
		tmp="Hold";
	}
	vocoder[filter][3]=tmp;
	//27
	vocoder[amp][0]=patchData[startAt+27];
	//28
	vocoder[amp][1]=patchData[startAt+28];
	//29
	vocoder[amp][2]=patchData[startAt+29]&0x01?"on":"off";
	//30
	// - velocity sense not used
	//31
	vocoder[amp][3]=patchData[startAt+31]-64;
	//32 to 35 
	// - not used (fixed value filter EG
	//36
	vocoder[aEG][0]=patchData[startAt+36];
	//37
	vocoder[aEG][1]=patchData[startAt+37];
	//38
	vocoder[aEG][2]=patchData[startAt+38];
	//39
	vocoder[aEG][3]=patchData[startAt+39];
	//40
	vocoder[lfo1][0]=lfo1Waves[patchData[startAt+40]&0x03];
	vocoder[lfo1][1]=lfoSync[(patchData[startAt+40]>>4)&0x03];
	//41
	vocoder[lfo1][3]=patchData[startAt+41];
	//42
	vocoder[lfo1][2]=patchData[startAt+42]&0x80?"on":"off";
	if(patchData[startAt+42]&0x80){
		//temp sync=on will over-write LFO freq with sync note
		vocoder[lfo1][3]=lfoSyncNote[patchData[startAt+42]&0x0F];
	}
	//43
	vocoder[lfo2][0]=lfo2Waves[patchData[startAt+43]&0x03];
	vocoder[lfo2][1]=lfoSync[(patchData[startAt+43]>>4)&0x03];
	//44
	vocoder[lfo2][3]=patchData[startAt+44];
	//45
	vocoder[lfo2][2]=patchData[startAt+45]&0x80?"on":"off";
	if(patchData[startAt+45]&0x80){
		//temp sync=on will over-write LFO freq with sync note
		vocoder[lfo2][3]=lfoSyncNote[patchData[startAt+45]&0x0F];
	}
	//level settings apply to pairs of channels
	//46
	vocoder[chleva][0]=patchData[startAt+46];
	//48
	vocoder[chleva][1]=patchData[startAt+48];
	//50
	vocoder[chleva][2]=patchData[startAt+50];
	//52
	vocoder[chleva][3]=patchData[startAt+52];
	//54
	vocoder[chlevb][0]=patchData[startAt+54];
	//56
	vocoder[chlevb][1]=patchData[startAt+56];
	//58
	vocoder[chlevb][2]=patchData[startAt+58];
	//60
	vocoder[chlevb][3]=patchData[startAt+60];	
	
	//pan settings apply to pairs of channels
	//62
	vocoder[chpana][0]=panText(patchData[startAt+62]);
	//64
	vocoder[chpana][1]=panText(patchData[startAt+64]);
	//66
	vocoder[chpana][2]=panText(patchData[startAt+66]);
	//68
	vocoder[chpana][3]=panText(patchData[startAt+68]);
	//70
	vocoder[chpanb][0]=panText(patchData[startAt+70]);
	//72
	vocoder[chpanb][1]=panText(patchData[startAt+72]);
	//74
	vocoder[chpanb][2]=panText(patchData[startAt+74]);
	//76
	vocoder[chpanb][3]=panText(patchData[startAt+76]);	
	
	//78-141 is EF Hold data. Not directly programmable.

}

//converts settings stored in array to slash-delimited string for display
function formatText(arr){
	var retval="";
	var l=arr.length;
	for(var j=0;j<l;j++){
		retval+=arr[j];
		if(j<l-1){
			retval+=" , ";
		}
	}
	retval+="\r\n";
	return retval;
}

//rescale 0-127.
function rescale(inVal, minVal, maxVal, asInt){
var v = minVal+(maxVal-minVal)*inVal/127;
if(asInt){
return v.toFixed(0);
}else{
 return v.toFixed(2);
}
}

//for an input value inVal, emit an output value with a centred zero and specified min/max
function reRange(inVal, absVal){
	var v=inVal-64;
	if(v==0){
		return 0;
	}else if(v>0){
		return Math.min(v,absVal);
	}else{
		return Math.max(v,-absVal);
	}
}

//take the stored Pan value and convert to L63...cnt...R63
function panText(pan){
	pan=pan-64; 
	if(pan==0){
		panpot="cnt";
	}else if(pan<0){
		panpot="L"+Math.abs(pan);
	}else{
		panpot="R"+pan;
	}	
	return panpot;
}


//this reads a chunk of 8 bytes in the .prg file (which is MIDI data)
//and converts them to the 7 bytes of message data that they encode
// see the microkorg MIDI implementation guide http://i.korg.com/uploads/Support/MK1_633652915168960000.pdf, Note 5 (data dump conversion)
function read8to7(data){
    var chunk = new Uint8Array(7);
    var bit7s = data[ptr];
    for(var i=0;i<7;i++){

        chunk[i] = ((bit7s & 0x01) ? 0x80 : 0x00) | data[i+ptr+1];
        bit7s = bit7s >> 1;
        //patchHex=patchHex+(ptr-ptr0+i)+": 0x"+chunk[i].toString(16)+" "+String.fromCharCode(chunk[i])+"\r\n";
        //alert(chunk[i].toString(16));
    }
    ptr+=8;
    return chunk;
}


function handleFileBrowse() {
  handleFile(document.getElementById("uploadInput").files[0]);
}

function handleFile(oFile){
  var nBytes = oFile.size;
  var sOutput = nBytes + " bytes";
  document.getElementById("fileSize").innerHTML = sOutput;

var reader = new FileReader();
reader.onloadend=function(){processData(reader.result);};
reader.readAsArrayBuffer(oFile);

}

//setup drop zone
function dragenter(e) {
  e.stopPropagation();
  e.preventDefault();
}
function dragover(e) {
  e.stopPropagation();
  e.preventDefault();
  filedrag.className="hover";
}
function drop(e) {
  e.stopPropagation();
  e.preventDefault();

  filedrag.className="";

  var dt = e.dataTransfer;
  var files = dt.files;

  handleFile(files[0]);
}

function Init(){
var dropbox;
dropbox = document.getElementById("filedrag");
dropbox.addEventListener("dragenter", dragenter, false);
dropbox.addEventListener("dragover", dragover, false);
dropbox.addEventListener("drop", drop, false);
}

