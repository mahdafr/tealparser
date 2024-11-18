import gradio as gr
import pandas as pd


def _read(f_path):
    return pd.read_csv(f_path, header=0)

def _to_string(df):
    return "Unique Company Names:\n{3}\n\
                \nUnique Role Titles:\n{2}\n\
                \nEntries:\n{0}\n\
                \nCharacters (incl. header row): {1}".format(
                                    df.to_string(index=False), # print the table w/out row #s
                                    len(df.to_string(index=False)), # total char count w/out row #s
                                    df.role.unique(), # unique roles
                                    df['company name'].unique()) # unique companies

def _filter_by(df_all, date, status):
    df_date = df_all.loc[df_all['date'] == date]
    return df_date.loc[df_date['event'] == status]

def _error_check(f_path, date, status):
    if f_path is None:
        raise gr.Error("No file selected. Please try again by selecting a CSV file to open.")
    if date is None:
        raise gr.Error("No date selected. Please try again by selecting a date to filter the data.")
    if status is None:
        raise gr.Error("No status selected. Please try again by selecting an application status to filter the data.")

def analyze(f_path, date, status_list):
    date = str(date.date())
    _error_check(f_path, date, status_list)
    df_all = _read(f_path)
    ret_str = "Date: {0}\n\n".format(date)
    for status in status_list:
        df = _filter_by(df_all, date, status)
        ret_str += "============{0}============\n\n{1}\n\n".format(status.upper(), _to_string(df, date))
    return ret_str


options = [
    ("Bookmarked", "bookmarked"),
    ("Applying", "applying"),
    ("Applied", "applied"),
    ("Interviewing", "interviewing"),
    ("Rejected", "not_selected"),
]

ui_elem = [gr.FileExplorer(label="CSV File", glob="*.csv", file_count="single"),
                gr.DateTime(label="Date to Examine", info="Filter the data to view only rows with this selected date", include_time=False, type="datetime"),
                gr.Dropdown(label="Application Status", multiselect=True, info="Filter the data to view only the selected application statuses", choices=options)]

demo = gr.Interface(
                    title="TealHQ Data Parsing",
                    description="Use this tool to analyze a job report exported from the TealHQ job tracker. This can be helpful for filing unemployment claims.",
                    fn=analyze,
                    inputs=ui_elem,
                    outputs=[gr.Textbox(label="Filtered Output")],
                    allow_flagging="never",
                    clear_btn=gr.ClearButton(components=ui_elem, value="Clear form"),
                    submit_btn=gr.Button(value="Filter", variant="primary"),
                    theme=gr.themes.Soft()
            )


demo.launch()
