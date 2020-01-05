from pytransdec import TransdecCommunication

with TransdecCommunication() as tc:
    # collect 1000 positive examples with noise of object 0
    tc.collect_data(positive=True, add_noise=True, add_background=False, n_images=1000,
                    save_dir='collected_data/{}/train'.format(0),
                    used_observations='all', object_number=0, show_img=True, draw_annotations=True)
    # collect 1000 positive examples with custom backgrount of object 0
    tc.collect_data(positive=True, add_noise=False, add_background=True, n_images=1000,
                    save_dir='collected_data/{}/train'.format(0),
                    used_observations='all', object_number=0, show_img=True, draw_annotations=True)
    # collect 1000 negative examples with noise of object 0
    tc.collect_data(positive=False, add_noise=True, add_background=False, n_images=1000,
                    save_dir='collected_data/{}/train'.format(0),
                    used_observations='all', object_number=0, show_img=True, draw_annotations=True)