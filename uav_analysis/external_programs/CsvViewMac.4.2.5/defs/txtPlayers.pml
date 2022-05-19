<?xml version="1.0"?>
<players>
	<sigPlayer>
		<name>Battery Temp C vs Consumption</name>
		<signal>
			<name>CNTR_BATT:temperature [C]</name>
			<color>Red</color>
		</signal>
		<signal>
			<name>SMART_BATTERY:volumeConsume</name>
			<color>black</color>
		</signal>
	</sigPlayer>
	<sigPlayer>
		<name>Battery Voltage and Percent Remaining</name>
		<Signal>
			<name>SMART_BATTERY:battery</name>
			<color>red</color>
		</Signal>
		<Signal>
			<name>SMART_BATTERY:voltage [V]</name>
			<color>black</color>
		</Signal>
	</sigPlayer>
		<sigPlayer>
		<name>Battery Voltage Per Cell</name>
		<Signal>
			<name>CNTR_BATT:voltageCell1 [V]</name>
			<color>red</color>
		</Signal>
		<Signal>
			<name>CNTR_BATT:voltageCell2 [V]</name>
			<color>black</color>
		</Signal>
		<Signal>
			<name>CNTR_BATT:voltageCell3 [V]</name>
			<color>blue</color>
		</Signal>
		<Signal>
			<name>CNTR_BATT:voltageCell4 [V]</name>
			<color>green</color>
		</Signal>
	</sigPlayer>
	<sigPlayer>
		<name>Distance Compared to Avail Time</name>
		<signal>
			<name>SMART_BATTERY:usefulTime [s]</name>
			<color>Red</color>
		</signal>
		<signal>
			<name>General:distance [m]</name>
			<color>black</color>
		</signal>
	</sigPlayer>
	<sigPlayer>
		<name>Forward Thrust Value over Distance</name>
		<signal>
			<name>RC:elevator</name>
			<color>black</color>
		</signal>
		<signal>
			<name>General:hSpeed [m/s]</name>
			<color>red</color>
		</signal>

	</sigPlayer>
	<sigPlayer>
		<name>flyCState:distance</name>
		<Signal>
			<name>General:flyCState</name>
			<color></color>
		</Signal>
		<Signal>
			<name>General:distance [m]</name>
		</Signal>
	</sigPlayer>
		<sigPlayer>
		<name>navHealth</name>
		<signal>
			<name>General:navHealth</name>
			<color>#ff0000</color>
			<stroke>thick</stroke>
		</signal>
		<signal>
			<name>General:numSats</name>
			<color>#00ff00</color>
			<stroke>thick</stroke>
		</signal>
		<signal>
			<name>General:flyCState</name>
			<color>#000000</color>
			<stroke>thin</stroke>
		</signal>
	</sigPlayer>
	<geoPlayer>
		<geopath>
			<name>AC</name>
			<Latitude>OSD:latitude</Latitude>
			<Longitude>OSD:longitude</Longitude>
			<Altitude>OSD:height [m]</Altitude>
			<headingSignal>OSD:yaw</headingSignal>
			<headingSignal>OSD:tiltDirection:C</headingSignal>
		</geopath>
		<geopath>
			<name>ImuCalcs</name>
			<default>dontDisplay</default>
			<Latitude>ImuCalcs:Lat:C</Latitude>
			<Longitude>ImuCalcs:Long:C</Longitude>
			<headingSignal>OSD:yaw</headingSignal>
		</geopath>
		<geopath>
			<name>Tablet</name>
			<Latitude>APP_GPS:latitude</Latitude>
			<Longitude>APP_GPS:longitude</Longitude>
		</geopath>
		<geopath>
			<name>RC</name>
			<Latitude>RC_GPS:latitude</Latitude>
			<Longitude>RC_GPS:longitude</Longitude>
		</geopath>
		<geopath>
			<name>HomePoint</name>
			<Latitude>HOME:latitude</Latitude>
			<Longitude>HOME:longitude</Longitude>
		</geopath>
	</geoPlayer>
</players>
