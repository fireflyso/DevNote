defaults
    mode            tcp
    log             global
    option          tcplog
    option          dontlognull
    option http-server-close
    option          redispatch
    retries         3
    timeout http-request 10s
    timeout queue   1m
    timeout connect 10s
    timeout client  1m
    timeout server  1m
    timeout http-keep-alive 10s
    timeout check   10s
    maxconn         3000

frontend    mysql
    bind        0.0.0.0:2222
    mode        tcp
    log         global
    default_backend test_server

backend     test_server
    balance roundrobin
    server mini 10.0.0.1:2222 check inter 5s rise 2 fall 3
    server mbp 10.0.0.2:2222 check inter 5s rise 2 fall 3

listen stats
    mode    http
    bind    0.0.0.0:1080
    stats   enable
    stats   hide-version
    stats uri /haproxyamdin?stats
    stats realm Haproxy\ Statistics
    stats auth admin:admin
    stats admin if TRUE


