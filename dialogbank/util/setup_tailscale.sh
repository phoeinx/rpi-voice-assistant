#following tailscale installation instructions for Raspberry Pi here: https://tailscale.com/kb/1197/install-rpi-bullseye

# 1. Install the apt-transport-https plugin
sudo apt-get install apt-transport-https

# 2. Add the Tailscale package signing key and repository
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list

# 3. Install Tailscale
sudo apt-get update
sudo apt-get install tailscale

# 4. Connect your machine to your Tailscale network and authenticate in your browser
sudo tailscale up