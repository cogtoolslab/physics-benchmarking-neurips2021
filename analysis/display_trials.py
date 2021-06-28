import os
from ipywidgets import Output, GridspecLayout
from IPython import display

# range is from 0 (min) to 1 (max)
# num is how many videos to display in a row
def plot_by_n(Dacc, video_dir, min, max, num=3):
    if max < 1:
        trials = Dacc[(Dacc["correct"]>=min) & (Dacc["correct"]<max)] # subset of the dominoes trials with corresponding accuracy
    else:
        trials = Dacc[(Dacc["correct"]>=min) & (Dacc["correct"]<=max)] # equal to max if it is 1
    trail_accu = trials["correct"].tolist() # corresponding accuracy for the trials
    trail_ans = trials["answer"].tolist() # corresponding ground truth for the trials
    video_ids = trials.index.tolist() # corresponding stim_IDs for the trials
    video_names = [i + '.mp4' for i in video_ids]
    video_paths = [os.path.join(video_dir,i) for i in video_names]

    # display videos with low accuracy 
    if (len(video_paths)%num != 0):
        grid = GridspecLayout(2 * (len(video_paths)//num + 1), num)
    else:
        grid = GridspecLayout(2 * (len(video_paths)//num), num)

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

        row_index = (i // num) * 2
        row_index_t = row_index + 1
        column_index = (i % num)
        column_index_t = column_index
        grid[row_index, column_index] = out
        grid[row_index_t, column_index_t] = out_t

    return grid