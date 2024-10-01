import gradio as gr
import pandas as pd


def _read(f_path):
    return pd.read_csv(f_path, header=0)

def _to_string(df):
    return "There are {0} characters to print including the header row.\n{1}".format(len(df.to_string()),
                                                                                                                       df.to_string())

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

def analyze(f_path, date, status):
    _error_check(f_path, date, status)
    df_all = _read(f_path)
    df = _filter_by(df_all, date, status)
    return _to_string(df)


options = [
    ("Bookmarked", "bookmarked"),
    ("Applying", "applying"),
    ("Applied", "applied"),
    ("Interviewing", "interviewing"),
]

ui_elem = [gr.FileExplorer(label="CSV File", glob="*.csv", file_count="single"),
                gr.DateTime(label="Date to Examine", info="Filter the data to view only rows with this selected date", include_time=False),
                gr.Dropdown(label="Application Status", info="Filter the data to view only this selected application status", choices=options)]

demo = gr.Interface(
                    title="TealHQ Data Parsing",
                    description="Use this tool to analyze a job report exported from the TealHQ job tracker. This can be helpful for filing unemployment claims.",
                    fn=analyze,
                    inputs=ui_elem,
                    outputs=[gr.Textbox(label="Filtered Output")],
                    allow_flagging="never",
                    clear_btn=gr.ClearButton(components=ui_elem, value="Clear form"),
                    submit_btn=gr.Button(value="Filter", variant="primary"),
                    theme=gr.themes.Soft())

demo.launch()
