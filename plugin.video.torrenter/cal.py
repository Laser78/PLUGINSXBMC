x = ['blabla.avi', 'lol\\sdasdas\\asdadas.xxxxt.avi', 'not lol\\sdasdas.xmpf']

import os
def foldername(path):
    if '\\' in path:
        foldername = path.split('\\')[0]
    else:
        foldername = ''
    return foldername

for y in x:
    print foldername(y)

#import libtorrent as lt
#import time, os
#
#def dump(obj):
#    for attr in dir(obj):
#        try:
#            print "'%s':'%s'," % (attr, getattr(obj, attr))
#        except:
#            pass
#
#ses = lt.session()
#ses.listen_on(6881, 6891)
#start_time=int(time.time())
#
#session_settings = ses.get_settings()
#session_settings['user_agent'] = 'uTorrent/3430(40298)'
#ses.set_settings(session_settings)
#
#e = lt.bdecode(open("D:\\105test.torrent", 'rb').read())
#info = lt.torrent_info(e)
##ses.set_alert_mask(lt.alert.category_t.all_categories)
#ses.set_alert_mask(lt.alert.category_t.storage_notification)
#ses.start_dht()
#ses.add_dht_router("router.bittorrent.com", 6881)
#ses.add_dht_router("router.utorrent.com", 6881)
#ses.add_dht_router("router.bitcomet.com", 6881)
#
##ses.start_dht()
#
#state_str = ['queued', 'checking', 'downloading metadata',
#        'downloading', 'finished', 'seeding', 'allocating']
#
#params = { 'save_path': 'D:\\',
#        #'storage_mode': lt.storage_mode_t.storage_mode_allocate,
#        'ti': info,}
#h = ses.add_torrent(params)
#for i in range(info.num_pieces()):
#    h.piece_priority(i, 0)
#for i in range(5,50):
#    h.piece_priority(i, 7)
#
#paused=False
#time.sleep(1)
#h.force_dht_announce()
#while True:
#    s = h.status()
#    ss = ses.status()
#    #print str(hh)+str(s.pieces)
#    #pr=h.piece_priorities()
#    #print str(pr)
#    dht_nodes = ss.dht_nodes#
#    dht_lookup = lt.dht_lookup()
#    is_dht_running='ON' if ses.is_dht_running() else 'OFF'
#    result='DHT: %s (%d)' % (is_dht_running, dht_nodes)#
#    trackers=[]
#    for tracker in h.trackers():
#        trackers.append((tracker['url'], tracker['fails'], tracker['verified']))
#    fails_sum, verified_sum = 0, 0
#    for url, fails, verified in trackers:
#        fails_sum+=fails
#        if verified: verified_sum+=1
#    result='  '+str(int(time.time())-start_time)+': '+result+' Trackers: verified %d/%d, fails=%d' %(verified_sum, len(trackers)-1, fails_sum)
#
#    #received=ses.pop_alert()
#    #while received:
#    #    print('[debug]: ['+str(type(received))+'] the alert '+str(received).decode('utf8').encode('cp1251')+' is received')
#    #    #if type(received) == self.lt.torrent_finished_alert:
#    #    #    self.session.pause()
#    #    received = ses.pop_alert()
#    if int(time.time())-start_time==20:
#        print 'force_dht_announce'
#        h.force_dht_announce()
#
#    if int(time.time())-start_time>40 and not paused:
#        paused=True
#        ses.pause()
#        print 'pause'
#
#    if int(time.time())-start_time==42:
#        ses.resume()
#        print 'resume'
#
#    #cache_status=ses.get_cache_status()
#    ###dump(cache_status)
#    #print str(cache_status.writes)+' '+str(cache_status.reads)
#
#    #p=[]
#    #for i in range(5):
#    #    if not h[hh].have_piece(i):
#    #        p.append(str(i)+'N')
#    #    else:
#    #        if i==1:
#    #            print h[hh].read_piece(1)
#    #        p.append('Y')
#    #print str(hh)+str(p)
#    #print h[hh].read_piece(1)
#
#    print '%s %.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %s' % \
#        (lt.version, s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
#        s.num_peers, s.num_pieces, str(s.state)) + str(result)
#
#
#    time.sleep(1)
#
#        #h[hh].save_resume_data()



