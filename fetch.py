import sys, os, optparse, traceback
import util, triphop
import notifier

opts = optparse.OptionParser(usage='fetch.py [OPTIONS] PATH',
                             description=__doc__)
opts.add_option('-c', '--cached', action='store_true',
                help='read input from cached files, for development')
opts.add_option('-n', '--dry-run', action='store_true',
                help='only print what would happen')

if __name__ == '__main__':
    ui = util.Ui()
    cfgpath = os.path.join(os.path.dirname(__file__), 'webupdates.cfg')
    ui.readconfig(cfgpath)

    options, args = opts.parse_args()
    (seenpath,) = args[:1]

    notifiers = {
        'email': notifier.Email,
        'twitter': notifier.Twitter,
        }
    apis = [
        (triphop.TripHopNet, 'samples/trip-hop.net', ['twitter']),
        ]

    notifications = {}
    seen = util.readseen(seenpath)
    notseen = []
    for apifn, path, notifs in apis:
        try:
            api = apifn(ui)
        except util.MissingConfigError, e:
            ui.info('missing configuration entry: %s\n' % str(e))
            continue
        html = None
        if options.cached:
            if not path:
                ui.info('skipping %s: no samples found\n' % api.name)
                continue
            html = file(path).read()
        try:
            updates = api.getupdates(html=html)
        except Exception, e:
            ui.error('Failed to get updates from %s\n' % api.name)
            ui.error(traceback.format_exc())
            continue
        updates = [u for u in updates if u[0] not in seen]
        for notif in notifs:
            notifications.setdefault(notif, []).extend(updates)
        for u in updates:
            if u[0] not in notseen:
                notseen.append(u[0])

    if not options.dry_run:
        util.addseen(seenpath, [u for u in notseen])

    for name, updates in notifications.iteritems():
        if not updates:
            continue
        notifierfn = notifiers.get(name)
        if not notifierfn:
            continue
        try:
            notifier = notifierfn(ui)
        except util.MissingConfigError, e:
            ui.info('missing configuration entry: %s\n' % str(e))
            continue
        data = '\n'.join(('%s: %s (%s)' % (name, label, url))
                         for (sid, label, url) in updates)
        data = (data + '\n').encode('utf-8')
        ui.info(data)
        if not options.dry_run:
            notifier.notify(updates)
