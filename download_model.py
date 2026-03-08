from huggingface_hub import snapshot_download

print("XTTS v2 model dosyaları indiriliyor (~2GB)...")
print("Bu işlem internet hızına bağlı olarak birkaç dakika sürebilir.\n")

snapshot_download(
    repo_id="coqui/XTTS-v2",
    local_dir="xtts_v2_local",
    local_dir_use_symlinks=False
)

print("\nİndirme tamamlandı! Artık sistem çevrimdışı çalışabilir.")