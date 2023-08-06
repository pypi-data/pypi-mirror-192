from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/bytetrack_from_videos",
    output_component_file="component.yaml",
)
def bytetrack_from_videos(
    input_video_dir: Input[Artifact],
    input_weights: Input[Artifact],
    output_video_dir: Output[Artifact],
    output_text_file_dataset_dir: Output[Dataset],
    output_video_dir_path: str,
    output_text_file_dataset_dir_path: str,
    device: str = "gpu",  # Must be gpu or cpu
):
    import os
    import pandas as pd
    import shutil
    from loguru import logger
    from tools.demo_track import make_parser, main, get_exp

    ################################
    # Helper functions
    ################################

    def setup_output_path(output_path):
        if output_path.startswith("gs://"):
            output_path_gs = output_path
            output_path_local = output_path.replace("gs://", "/gcs/")
        elif output_path.startswith("/gcs/"):
            output_path_gs = output_path.replace("/gcs/", "gs://")
            output_path_local = output_path
        else:
            raise ValueError("output_path should start with either gs:// or /gcs/")
        return output_path_gs, output_path_local

    ################################
    # Setup output paths
    ################################

    output_video_dir_path_gs, output_video_dir_path_local = setup_output_path(
        output_video_dir_path
    )
    output_video_dir_local = os.path.dirname(output_video_dir_path_local)
    os.makedirs(output_video_dir_local, exist_ok=True)
    (
        output_text_file_dataset_dir_path_gs,
        output_text_file_dataset_dir_path_local,
    ) = setup_output_path(output_text_file_dataset_dir_path)
    output_text_file_dataset_dir_local = os.path.dirname(
        output_text_file_dataset_dir_path_local
    )
    # output_text_file_dataset_dir_local = os.path.dirname(
    #     output_text_file_dataset_path_local
    # )
    os.makedirs(output_text_file_dataset_dir_local, exist_ok=True)

    output_video_dir.uri = output_video_dir_path_gs
    output_text_file_dataset_dir.uri = output_text_file_dataset_dir_path_gs

    # List the videos in the input directory
    file_names = os.listdir(input_video_dir.path)
    file_paths = [
        os.path.join(input_video_dir.path, file_name) for file_name in file_names
    ]
    file_names_and_paths = list(zip(file_names, file_paths))

    ################################
    # Run bytetrack
    ################################

    for file_name_and_path in file_names_and_paths:
        logger.info(f"Processing {file_name_and_path[1]}")
        # Create arguments for bytetrack
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--path",
            file_name_and_path[1],
            "--fuse",
            "--save_result",
        ]
        if device == "gpu":
            arg_list += ["--fp16"]
        elif device == "cpu":
            arg_list += ["--device", "cpu"]
        # Run bytetrack
        args = make_parser().parse_args(arg_list)
        exp = get_exp(args.exp_file, args.name)
        main(exp=exp, args=args)
        # Copy outputs to GCS
        source_dir = "/ByteTrack/YOLOX_outputs/yolox_x_mix_det/track_vis"
        source_video = f"{source_dir}/output.mp4"
        source_results = f"{source_dir}/results.txt"
        output_video_dir_path_local = os.path.join(
            output_video_dir_local, file_name_and_path[0]
        )
        output_text_file_dataset_path_local = (
            os.path.join(output_text_file_dataset_dir_local, file_name_and_path[0])
            + ".csv"
        )
        shutil.copyfile(source_video, output_video_dir_path_local)
        shutil.copyfile(source_results, output_text_file_dataset_path_local)

    # output_text_file_dataset_dir.path = os.path.join(
    #     output_text_file_dataset_dir_local, "data.csv"
    # )

    # # Combine all the results into a single csv file
    # file_paths = [
    #     os.path.join(output_text_file_dataset_dir_local, file_name)
    #     for file_name in os.listdir(output_text_file_dataset_dir_local)
    # ]
    # dfs = [pd.read_csv(file_path, header=None) for file_path in file_paths]
    # df_shapes = [df.shape for df in dfs]
    # logger.info(f"df_shapes: {df_shapes}")
    # df = pd.concat(dfs)
    # df.to_csv(output_text_file_dataset.path, index=False)
