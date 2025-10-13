import os
import shutil

from metaflow import Flow, profile, current


def fix_symlinks(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            path = os.path.join(dirpath, name)
            if os.path.islink(path):
                target = os.readlink(path)
                abs_target = os.path.abspath(
                    os.path.join(os.path.dirname(path), target)
                )
                if not os.path.exists(abs_target):
                    raise Exception(f"Unexpected broken symlink: {path} -> {target}")
                if os.path.isdir(abs_target):
                    raise Exception(f"Unexpected directory symlink: {path} -> {target}")
                os.remove(path)
                os.rename(abs_target, path)

    for dirpath, dirnames, _ in os.walk(root_dir, topdown=True):
        for dirname in dirnames[:]:
            if dirname == "blobs":
                full_path = os.path.join(dirpath, dirname)
                shutil.rmtree(full_path, ignore_errors=True)
                return


def load():
    existing = list(Flow("ProductImageFlow").runs("model-checkpoint"))
    if existing:
        run = existing[0]
        print(f"Loading existing checkpoint from {run}")
        return run["start"].task.data.model_checkpoint
    else:
        print("No existing checkpoints found - creating a new one")
        from imggen import ImgGen

        gen = ImgGen()
        gen.load_model(only_load=True)
        fix_symlinks("/model")
        with profile("Saving checkpoint"):
            checkpoint = current.checkpoint.save(path="/model")
        Flow("ProductImageFlow")[current.run_id].add_tag("model-checkpoint")
        print("Checkpoint created!")
        return checkpoint
