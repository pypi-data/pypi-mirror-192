import torch

ckpt1 = torch.load("/user/HS502/hl01486/.cache/audioldm/audioldm-s-full.ckpt", map_location="cpu")["state_dict"]
ckpt2 = torch.load("/mnt/fast/nobackup/users/hl01486/projects/general_audio_generation/AudioLDM-python/audioldm-s-full", map_location="cpu")["state_dict"]

for k in ckpt1.keys():
    if(torch.mean(torch.abs(ckpt1[k].float() - ckpt2[k].float())) < 1e-5):
        continue
    else:
        print(k)
        import ipdb;ipdb.set_trace()
        