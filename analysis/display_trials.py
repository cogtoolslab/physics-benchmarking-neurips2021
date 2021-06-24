import os
from ipywidgets import Output, GridspecLayout
from IPython import display

def plot_by_3(Dacc, video_dir):
    trials_33 = Dacc[Dacc["correct"]<=0.33] # subset of the dominoes trials with 33.3% or lower accuracy
    trail_accu = trials_33["correct"].tolist() # corresponding accuracy for the trials
    trail_ans = trials_33["answer"].tolist() # corresponding ground truth for the trials
    video_ids = trials_33.index.tolist() # corresponding stim_IDs for the trials
    video_names = [i + '.mp4' for i in video_ids]
    video_paths = [os.path.join(video_dir,i) for i in video_names]

    # display videos with low accuracy 
    if (len(video_paths)%3 != 0):
        grid = GridspecLayout(2 * (len(video_paths)//3 + 1), 3)
    else:
        grid = GridspecLayout(2 * (len(video_paths)//3), 3)

    for i, filepath in enumerate(video_paths):
        # display videos
        out = Output()
        with out: 
            display.display(display.Video(filepath, embed=True, width=360, height=360))

        # display related info in text form
        out_t = Output()
        content = "The accuracy of this trail is " + str(round(trail_accu[i]*100, 3)) + " % " + "(" + ('hit the yellow area' if trail_ans[i] else 'Not hit the yellow area') + ")"


        with out_t:
            display.display(display.Markdown(data = content))

        row_index = (i // 3) * 2
        row_index_t = row_index + 1
        column_index = (i % 3)
        column_index_t = column_index
        grid[row_index, column_index] = out
        grid[row_index_t, column_index_t] = out_t

    return grid