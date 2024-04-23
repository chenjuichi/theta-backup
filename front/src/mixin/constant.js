// Add more constants as needed
export const SYSTEM = 1;

export const _thetaEmpIDLength = 4;
export const _thetaPassword = 'a1234';
export const _thetaPasswordMaxLength = 6;
export const _thetaPasswordMinLength = 4;
export const _thetaPrimaryColor = '#5a96cc';

export const _thetaSpindleTypes = [
	'內藏式高速銑削/研磨用主軸',										//TH, THN, THS,
	'內藏式高速銑削/研磨用主軸(FANUC內藏式馬達)',		//TH, TT, THN
	'內藏式車銑複合主軸',													//THS, TTS
	'內藏式雕刻機用主軸',		//TH, THZ
	'內藏式內孔研磨用主軸',	//THG, THGZ
	'內藏式研磨用主軸',			//THG, THGN, THGA, THGAS
	'皮帶式研磨用主軸',			//THGSD
	'內藏式砂輪修整主軸',		//THGA, THGZ, THGL,TTGZ, TTGD
	'皮帶式修砂主軸',				//THSGD, THAV,THSG
];

export const _thetaLubrications = [
	' ', '油氣潤滑', '油脂潤滑',
];

export const _thetaCoolings = [
	' ', '水冷/油冷',
];

export const _thetaSpindleOuters = [
	'80', '110','120', '150', '170', '190','200', '210','230','255', '310',
];
//刀把介面
export const _thetaHandles = [
	//' ',							//0
	'客製化',						//1
	'BT-30 BBT-30',
	'BT-40 BBT-40',
	'Collet 3.175~6mm',				//4
	'D36/63	HSK-C50',
	'D36/68 HSK-C63',
	'D36/68 D36/78 HSK-C63',
	'EB-20(1:6)',
	'HSK-A63 BBT-40',
	'HSK-E20',						//10
	'HSK-E25 ISO-15',
	'HSK-E32',
	'HSK-E40 BBT-30',
	'HSK-E40 HSK-F50',
	'HSK-E50 HSK-F63',
	'HSK-A63 HSK-E63',
	'HSK-T63 Capto C6',
	'ISO-20',
	'ISO-25',
	'WT-5(Collet 1~6mm)',			//20
	'Ø60/48 M32X1.5P',
	'Ø57/72.5 M35X1.5P',
	'Ø66.8/69',
	'Ø72/95 M35X1.5P',				//24
];

export const _thetaSpindleTypeAndID = [
	'All',
	'銑削/研磨主軸(自動換刀) THZ-62.03',										//TH, THN, THS,
	'銑削/研磨主軸(自動換刀) THZ-62.05',										//TH, THN, THS,
	'銑削/研磨主軸(自動換刀) THZ-62.06',										//TH, THN, THS,
	'銑削/研磨主軸(自動換刀) THZ-80.01',										//TH, THN, THS,
	'銑削/研磨主軸(自動換刀) TH-120.08',										//TH, THN, THS,
	'研磨主軸(手動換刀) THG-80.01',		//TH, TT, THN
	'研磨主軸(手動換刀) THG-80.02',		//TH, TT, THN
	'研磨主軸(手動換刀) THG-80.03',		//TH, TT, THN
	'研磨主軸(手動換刀) THG-100.01',													//THS, TTS
	'研磨主軸(手動換刀) THG-100.03',		//TH, THZ
	'修砂主軸(手動換刀) THGA-V50.01',	//THG, THGZ
	'修砂主軸(手動換刀) THGA-V60.01',			//THG, THGN, THGA, THGAS
	'修砂主軸(手動換刀) THGL-60.01',			//THGSD
	'修砂主軸(手動換刀) THGA-V50.01',		//THGA, THGZ, THGL,TTGZ, TTGD
	'修砂主軸(手動換刀) THGA-60.01',				//THSGD, THAV,THSG
	'修砂主軸(手動換刀) THGL-60.01',				//THSGD, THAV,THSG
];
//馬達種類
export const _thetaSpindleMotorType = [
	'空白',
	'1.5',
	'10',
	'15',
	'16',
	'18',
	'20',
	'15/18.5',
	'18.5/22',
	'30',
	'FANUC BiI 56L/40000',
	'FANUC BiI 40M/70000',
	'FANUC BiI 50L/30000',
];
//馬達功率
export const _thetaSpindleS1Kw = [
	'3.0',
	'7.5',
	'10',
	'18',
	'30',
];
//馬達扭力
export const _thetaSpindleS1Nm = [
	'0.95',
	'4.77',
	'5.9',
	'29.1',
	'29.3',
];

// Function to create CSS with constants
export function _createCSSWithConstants() {
	const style = document.createElement('style');
	style.innerHTML = `
		:root {
			--navbar-header-color: ${_thetaPrimaryColor};
		}
	`;

	document.head.appendChild(style);
}