<?xml version="1.0"?>
<players>
	
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
