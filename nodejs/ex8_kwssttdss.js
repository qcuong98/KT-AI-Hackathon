const record=require('node-record-lpcm16');
const aikit=require('./aimakerskitutil');
const Speaker=require('speaker');
const fs=require('fs');

//node version check
const nodeVersion=process.version.split('.')[0];
let ktkws=null;
if(nodeVersion==='v6') ktkws=require('./ktkws');
else if(nodeVersion==='v8') ktkws=require('./ktkws_v8');

//for playing pcm sound
const soundBuffer=fs.readFileSync('../data/sample_sound.wav');
const pcmplay=new Speaker({
	channels:1,
	bitDepth:16,
	sampleRate:16000
});


const client_id='';
const client_key='';
const client_secret='';
const json_path='';
const cert_path='../data/ca-bundle.pem';
const proto_path='../data/gigagenieRPC.proto';

const kwstext=['기가지니','지니야','친구야','자기야'];
const kwsflag=parseInt(process.argv[2]);
let pcm=null;
function initMic(){
        return record.start({
                sampleRateHertz: 16000,
                threshold: 0,
                verbose: false,
                recordProgram: 'arecord',
        })
};
ktkws.initialize('../data/kwsmodel.pack');
ktkws.startKws(kwsflag);
let mic=initMic();

//aikit.initialize(client_id,client_key,client_secret,cert_path,proto_path);
aikit.initializeJson(json_path,cert_path,proto_path);

let mode=0;//0:kws, 1:stt
let ktstt=null;
mic.on('data',(data)=>{
	if(mode===0){
		result=ktkws.pushBuffer(data);
		if(result===1) {
			console.log("KWS Detected");
			pcmplay.write(soundBuffer);
			setTimeout(startQueryVoice,1000);
		}
	} else {
    		ktstt.write({audioContent:data});
	}
});
console.log('say :'+kwstext[kwsflag]);

function startQueryVoice(){
	ktstt=aikit.queryByVoice((err,msg)=>{
		if(err){
			console.log(JSON.stringify(err));
			mode=0;
		} else {
			console.log('Msg:'+JSON.stringify(msg));
			const action=msg.action[0];
			if(action){
				const actType=action.actType;
				const mesg=action.mesg;
				console.log('actType:'+actType+' mesg:'+mesg);
				if(actType==='99' || actType==='601' || actType==='631' || actType==='607' || actType==='608' || actType==='606'){
					let kttts=aikit.getText2VoiceStream({text:mesg,lang:0,mode:0});
					kttts.on('error',(error)=>{
						console.log('Error:'+error);
					});
					kttts.on('data',(data)=>{
						if(data.streamingResponse==='resOptions' && data.resOptions.resultCd===200) console.log('Stream send. format:'+data.resOptions.format);
						if(data.streamingResponse==='audioContent') {
							pcmplay.write(data.audioContent);
						} else console.log('msg received:'+JSON.stringify(data));
					});
					kttts.on('end',()=>{
						console.log('pcm end');
						mode=0;
					});
				} else mode=0
			} else mode=0;
		}
	});
	ktstt.write({reqOptions:{lang:0,userSession:'12345',deviceId:'D06190914TP808IQKtzq'}});
	mode=1;
};
