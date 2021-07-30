/*

{
	"siteID" : "BK005",
	"timestamp" : 1611942541,
	"waterSensorData" : {
		"Level" : -0.3189875,
		"Flow" : 0,
		"Temperature" : 0,
		"ElectricalConductivity" : 0,
		"Salinity" : 14.743749999999999
	},
	"powerMeterData" : {
		"Voltage" : 1,
		"Current" : 0,
		"Power" : 0,
		"Energy" : 0
	},
	"status" : {
		"ACPowerOK" : true,
		"BatteryLow" : false,
		"CabTamper" : false,
		"SurgeProtectionFailure" : false
	}
}

*/

//Site ID, ระดับน้ำ sensor, ระดับน้ำทะเลปานกลาง
data = JsonConvert.DeserializeObject<DataLogging>(json);

var levelRef = 1.0;
var meanseaRef = 0.0; 
switch (data.SiteID){
	case "BK002": //สถานีวัดกองแก้ว
		data.SiteID = "IN01";
		levelRef = 2.36;
		meanseaRef = 1.912; //2.36
		break;
	case "BK005": //สถานีสวนศรีนครเขื่อนขันธ์
		data.SiteID = "IN02";
		levelRef = 2.43;
		meanseaRef = 0.887; //2.43
		break;
	case "BK004": //สถานีคลองลัดบางยอ
		data.SiteID = "IN04";
		levelRef = 2.00;
		meanseaRef = 1.852; //2.00
		break;
	case "BK008": //สถานีประตูระบายน้ำคลองตาสัก
		data.SiteID = "OT01";
		levelRef = 4.13;
		meanseaRef = 2.256; //2.42
		break;
	case "BK003": //สถานีประตูระบายน้ำคลองวัดบางกระเจ้านอก
		data.SiteID = "OT02";
		levelRef = 4.4;
		meanseaRef = 1.689; //2.15
		break;
	case "BK006": //สถานีประตูระบายน้ำคลองบางน้ำผึ้งนอก
		data.SiteID = "OT03";
		levelRef = 3.66; //1.95
		meanseaRef = 2.208; //2.25
		break;
	case "BK007": //สถานีประตูระบายน้ำคลองยายบ่าย
		data.SiteID = "OT04";
		levelRef = 4.11;
		meanseaRef = 1.484; //2.24
		break;
	case "BK001": //สถานีประตูระบายน้ำคลองแพ
		data.SiteID = "OT05";
		levelRef = 4.8;
		meanseaRef = 1.864; //2.43
		break;
	default:
		//data.SiteID = "Error";
		break;
}

// คำนวณค่าจาก Sensor เป็นค่าจริงที่แสดงบน web
if (data.WaterSensorData.Level < 400){
	data.WaterSensorData.Level = 400;
}
data.WaterSensorData.Level = ((data.WaterSensorData.Level - 400.0) * (levelRef / 1600.0)) - meanseaRef;
	
if (data.WaterSensorData.Salinity < 400){
	data.WaterSensorData.Salinity = 400;
}
data.WaterSensorData.Salinity = (data.WaterSensorData.Salinity - 400.0) * (70 / 1600.0);
	
if (data.WaterSensorData.Temperature < 400){
	data.WaterSensorData.Temperature = 400;
}
data.WaterSensorData.Temperature = (data.WaterSensorData.Temperature - 400.0) * (200 / 1600.0);