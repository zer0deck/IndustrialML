import pandas as pd

import folium
from folium import plugins

def print_marks(dataframe: pd.DataFrame):
    # Prepare dataset, remain only lon. lat and zero column
    stats = dataframe.groupby(['lon','lat'])[dataframe.columns[0]].count().reset_index().sort_values(dataframe.columns[0])

    spb_map = folium.Map(location=(59.93863, 30.31413), tiles="openstreetmap", zoom_start=10)

    figure_both = folium.FeatureGroup(name="Map with publications").add_to(spb_map)


    for coords in stats[['lat','lon']].values:
        folium.Marker(tuple(coords), tooltip='mark', popup = "point").add_to(figure_both)

    folium.LayerControl(collapsed=False).add_to(spb_map)

    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    mouse_position = folium.plugins.MousePosition(
        position='topright',
        separator=' Long: ',
        empty_string='NaN',
        lng_first=False,
        num_digits=20,
        prefix='Lat:',
        lat_formatter=formatter,
        lng_formatter=formatter,
    )

    spb_map.add_child(mouse_position)

    return spb_map