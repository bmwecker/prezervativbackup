# VPN Infrastructure Backup - Full Knowledge Transfer

This repository contains a full backup of knowledge and skills for setting up a personal VPN infrastructure to bypass censorship. It is designed to allow any agent or person to recreate the system from scratch.

## [Architecture] System Architecture

[Client (Hiddify/Xray)] 
        | (VLESS + Reality, port 443)
        [Yandex Cloud Relay VM] - Russian IP, pre-emptible
           (iptables DNAT -> 45.148.118.5:443)
                   |
                   [Swedish VPS - 45.148.118.5] - 3X-UI panel, Xray core
                           | (for Google/Claude/NotebookLM)
                              [Cloudflare WARP] - Unique IP, geo-bypass
                                      |
                                         [Internet]

                                         ## [Parameters] Current Infrastructure Parameters

                                         | Component | Value |
                                         |-----------|-------|
                                         | Main Server (VPS) | 45.148.118.5 (Switzerland, JustHost) |
                                         | Management Panel | https://45.148.118.5:31208/V0dEU3CRUVn1z3MgHn/ |
                                         | Panel Login | iYdrvxh6Mg |
                                         | Panel Password | mjK6Afc7yi |
                                         | DuckDNS Domain | prezervativ.duckdns.org |
                                         | DuckDNS Token | de9aab33-2808-49a1-a10f-d211121f7dff |
                                         | VLESS UUID | 462877e4-2d3e-47a2-ba1c-efd4cbce14fe |
                                         | Reality PublicKey | WmoRX8YHYK0wzDMyaZQip2rwz3-1P2SIRzbgU--QiGg |
                                         | Reality ShortID | 4cc90bb2dd |
                                         | Reality SNI | www.microsoft.com |

                                         ### VLESS Connection Link
                                         vless://462877e4-2d3e-47a2-ba1c-efd4cbce14fe@prezervativ.duckdns.org:443?type=tcp&encryption=none&security=reality&pbk=WmoRX8YHYK0wzDMyaZQip2rwz3-1P2SIRzbgU--QiGg&fp=chrome&sni=www.microsoft.com&sid=4cc90bb2dd&spx=%2F

                                         ## [Structure] Repository Structure

                                         - docs/ - step-by-step guides for each layer
                                         - scripts/ - Python scripts for automation
                                         - configs/ - ready-to-use Xray configs
                                         - windows/ - .bat files for Windows client

                                         ## [Troubleshooting] Common Issues

                                         | Symptom | Cause | Solution |
                                         |---------|-------|----------|
                                         | location=unsupported on notebooklm | Xray SNI sniffing disabled | Run enable_sniffing.py |
                                         | Network Error in 3X-UI | Xray failed due to bad config | SSH -> systemctl restart x-ui |
                                         | Shows Russian IP | VPN disconnected or DNS leak | Check client + DNS |
                                         | Yandex relay down | VM restarted, new IP | Check prezervativ.duckdns.org |
                                         
