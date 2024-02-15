import schedule
import streamlit as st
import pandas as pd
from webapp_supabase import SupaDatabase

st.set_page_config(
    page_title="Project Agriflow",
    page_icon="🎓",
    layout="centered",
)
st.title("🎓 Project Agriflow")
st.header('Hello, This is Project AgriFlow Web Assistant')

st.subheader("Real Time Weather Data...")


def real_time_data_show():
    with st.container(border=True):
        a89 = SupaDatabase()
        realdata89 = a89.real_time_data()
        st.error("Real Time Weather Data. Please reload the Browser to see Real Time 'Weather Data'.")

        raindetect = a89.rain_data()
        if raindetect[0]['Rain'] == 0:
            st.info("☀️ No significant rain expected.")
        else:
            st.info("🌧️ It can be Raining today.")

        with st.container(border=True):
            tem65 = realdata89[0]["Temperature"]
            st.slider("Temperature", 0, 100, int(tem65))
            if 10 <= tem65 < 20:
                st.info("Weather is Too cold.")
            elif 20 <= tem65 <= 25:
                st.info("Weather is Cold.")
            elif 25 <= tem65 <= 33:
                st.info("Beautiful Weather.")
            elif 33 <= tem65 <= 40:
                st.info("Weather is Hot.")
            else:
                st.info("Weather is Too Hot.")

        with st.container(border=True):
            mos65 = realdata89[0]["Moisture"]
            st.slider("Moisture", 0, 100, int(mos65))

        with st.container(border=True):
            hum65 = realdata89[0]["Humidity"]
            st.slider("Humidity", 0, 100, int(hum65))

        with st.container(border=True):
            pre65 = realdata89[0]["Pressure"]
            st.slider("Pressure", 0, 200000, int(pre65))


st.markdown("***")

show_current_info = st.button("Show Current Sensor Data", key="01SensorData")
if show_current_info:
    a = SupaDatabase()
    realdata = a.real_time_data()
    pdframe = pd.DataFrame(realdata)
    st.dataframe(pdframe)

st.markdown("***")


def tab_status():
    st.header("Water Status")
    a1 = SupaDatabase()
    data = a1.supabase_data_get()

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Water Status", "Pump", "Led"])

    # Content for each tab
    with tab1:
        if data[0]["WaterOut"] == 1:
            st.warning("Water is Dropping.")
            st.info("Pump is ON.")
            bcs01 = st.button("Turn Off Pump", key="02Pumpoff")
            if bcs01:
                a1.sensorout_update("WaterOut", 0)
                st.success("Pump is off")
        else:
            st.success("1. Water is Under Control.")
            st.info("Pump is OFF.")
            bcs02 = st.button("Turn On Pump", key="03PumpOn")
            if bcs02:
                a1.sensorout_update("WaterOut", 1)
                st.success("Pump is On")

    with tab2:
        if data[0]["WaterIn"] == 1:
            st.warning("Field is dired.")
            st.info("Pump is ON.")
            bcs03 = st.button("Turn Off Pump", key="04Pumpoff")
            if bcs03:
                a1.sensorout_update("WaterIn", 0)
                st.success("Pump is off")
        else:
            st.success("Field is Under Control.")
            st.info("Pump is OFF.")
            bcs04 = st.button("Turn On Pump", key="05PumpOn")
            if bcs04:
                a1.sensorout_update("WaterIn", 1)
                st.success("Pump is On")
    with tab3:
        if data[0]["LedStatus"] == 1:
            st.warning("It's Night.")
            st.info("LED is ON.")
            bcs05 = st.button("Turn Off LED", key="06LEDOff")
            if bcs05:
                a1.sensorout_update("LedStatus", 0)
                st.success("LED is off")
        else:
            st.success("It's Day.")
            st.info("LED is OFF.")
            bcs06 = st.button("Turn On LED", key="07LEDon")
            if bcs06:
                a1.sensorout_update("LedStatus", 1)
                st.success("Pump is On")


def sensor_status():
    st.header("Sensor Status")
    a2 = SupaDatabase()
    data3 = a2.sensor_data()
    pdframe1 = pd.DataFrame(data3)

    # Create tabs
    Temperature, Pressure, Moisture, Humidity = st.tabs(["Temperature", "Pressure", "Moisture", "Humidity"])

    # Content for each tab
    with Temperature:
        st.write("Temperature Status: ")
        temframe = pdframe1[["Date", "Temperature"]]
        st.dataframe(temframe)
        tem1 = pdframe1["Temperature"]
        st.bar_chart(tem1)

    with Pressure:
        st.write("Pressure Status: ")
        temframe = pdframe1[["Date", "Pressure"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Pressure"]
        st.bar_chart(tem1)

    with Moisture:
        st.write("Moisture Status: ")
        temframe = pdframe1[["Date", "Moisture"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Moisture"]
        st.bar_chart(tem1)

    with Humidity:
        st.write("Humidity Status: ")
        temframe = pdframe1[["Date", "Humidity"]]
        st.dataframe(temframe.set_index("Date"))
        tem1 = pdframe1["Humidity"]
        st.bar_chart(tem1)

    st.markdown("***")
    command_input = st.text_input("Enter your Command : ")
    if "who are you" in command_input.lower():
        st.info("I am Project Agriflow. I can do multiple task on Agricultural farm.")
    elif command_input:
        st.info("I am not configured yet.")

    st.info("💡 I am command based model. You can control me by writing command.")


st.markdown("""<html><head>
<style>
div.st-emotion-cache-1inwz65.ew7r33m0 {
display: none;
}
</style>
</head><body><body></html>
""", unsafe_allow_html=True)

real_time_data_show()
tab_status()
sensor_status()

# schedule.every(20).seconds.do(real_time_data_show)
# while True:
#     schedule.run_pending()
