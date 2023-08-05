from simba.misc_tools import check_file_exist_and_readable, get_video_meta_data, find_all_videos_in_directory
from simba.unsupervised.misc import check_directory_exists, read_pickle
from simba.rw_dfs import read_df

class ClusterVisualizer(object):
    def __init__(self,
                 video_dir: str,
                 data_path: str,
                 settings: dict or None):

        check_file_exist_and_readable(file_path=data_path)
        self.video_files = find_all_videos_in_directory(video_dir)
        self.data = read_pickle(data_path=data_path)
        self.cluster_ids = self.data['DATA']['CLUSTER'].unique()


    def create(self):
        for cluster_id in self.cluster_ids:
            cluster_df = self.data['DATA'][self.data['DATA']['CLUSTER'] == cluster_id]
            for video_name in cluster_df['VIDEO'].unique():
                video_cluster_df = cluster_df[cluster_df['VIDEO'] == video_name]
                pass


settings = {'video_speed': 0.4}


test = ClusterVisualizer(video_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/project_folder/videos',
                      data_path='/Users/simon/Desktop/envs/troubleshooting/unsupervised/dr_models/dreamy_spence_awesome_elion.pickle',
                      settings={})
test.create()
