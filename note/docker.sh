docker run -itd --name slb_monitor_agent -v /data:/data -v /etc/hosts:/etc/hosts slb_monitor_agent



docker run -itd --name slb_monitor_handle -e SRC_IP=REGISTER_ID -v /data:/data -v /etc/hosts:/etc/hosts slb_monitor_handle