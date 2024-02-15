import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode, ColumnsAutoSizeMode

st.set_page_config(layout="wide")

@st.cache_data()
def data_upload():
    df = pd.read_csv('./Superstore_min.csv')
    return df

df = data_upload()

# st.header("This is Streamlit Dataframe")
# st.dataframe(data=df)
# st.info(len(df))

_funct = st.sidebar.radio(label="Functions", options=['Display','Highlight','Delete'])

st.header("This is AgGrid Table with Pagination")

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True)
gd.configure_default_column(editable=False,groupable=True)

if _funct=='Display':
    sel_mode=st.radio('Selection Type',options=['single','multiple'])
    gd.configure_selection(selection_mode=sel_mode,use_checkbox=True)
    gd.configure_side_bar()    # SIDEBAR
    gridoptions=gd.build()

    grid_table=AgGrid(df, gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            allow_unsafe_jscode=True,
            height=400,
            ## Pagination
            custom_css={
                    "#gridToolBar": {
                        "padding-bottom": "0px !important",
                    }
                },
            theme='balham', # streamlit | alpine | balham | material
    )
    st.info("Total Rows :" + str(len(grid_table['data'])))   
    
    sel_row = grid_table["selected_rows"]
    st.subheader("Output")
    st.write(sel_row)







if _funct=='Highlight':
    col_opt=st.selectbox(label='Select column',options=df.columns, index=df.columns.get_loc('Category'))
    cellstyle_jscode=JsCode("""
        function(params){
            if (params.value == 'Furniture') {
                return{
                    'color': 'black',
                    'backgroundColor': 'orange'
                }
            }
            if (params.value == 'Office Supplies') {
                return{
                    'color'  : 'black',
                    'backgroundColor' : 'red'
                }
            }
            else{
                return{
                    'color': 'black',
                    'backgroundColor': 'lightpink'
                }
            }
                            
        };
    """
    )

    gd.configure_columns(col_opt, cellStyle=cellstyle_jscode)
    gd.configure_side_bar()    # SIDEBAR

    gridOptions = gd.build()
    grid_table = AgGrid(df, 
            gridOptions = gridOptions, 
            enable_enterprise_modules = True,
            # fit_columns_on_grid_load = True,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            height=400,
            width='100%',
            # theme = "material",
            update_mode = GridUpdateMode.SELECTION_CHANGED,
            reload_data = True,
            allow_unsafe_jscode=True,
            ## Pagination
            custom_css={
                    "#gridToolBar": {
                        "padding-bottom": "0px !important",
                    }
                },
            )
    





if _funct == 'Delete':
    js = JsCode("""
    function(e) {
        let api = e.api;
        let sel = api.getSelectedRows();
        api.applyTransaction({remove: sel})    
    };
    """     
    )  
    
    gd.configure_selection(selection_mode= 'single')
    gd.configure_side_bar()    # SIDEBAR
    gd.configure_grid_options(onRowSelected = js,pre_selected_rows=[])
    gridOptions = gd.build()
    grid_table = AgGrid(df, 
                gridOptions = gridOptions, 
                enable_enterprise_modules = True,
                fit_columns_on_grid_load = True,
                height=400,
                width='100%',
                # theme = "streamlit",
                update_mode = GridUpdateMode.SELECTION_CHANGED,
                # reload_data = True,
                allow_unsafe_jscode=True,
                ## Pagination
                custom_css={
                        "#gridToolBar": {
                            "padding-bottom": "0px !important",
                        }
                    },
                )   
    st.balloons()
    st.info("Total Rows :" + str(len(grid_table['data'])))   