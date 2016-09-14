## Latest/current build will be the Circleci API response

What responses look like from the circleci API response.

# a running build
(u'branch: dependency-graph', 'vcs_tag: None', u'lifecycle: running', 'outcome: None', u'status: running', 'stop_time: None')

# finished successful build
(u'branch: dependency-graph', 'vcs_tag: None', u'lifecycle: finished', 'outcome: success', u'status: success', 'stop_time: 2016-09-07T09:19:48.198Z')

# fixed build
(u'branch: master', 'vcs_tag: None', u'lifecycle: finished', 'outcome: success', u'status: fixed', 'stop_time: 2016-09-01T11:37:45.806Z')

# failed build
(u'branch: master', 'vcs_tag: None', u'lifecycle: finished', 'outcome: failed', u'status: failed', 'stop_time: 2016-09-01T10:48:14.795Z')

# cancelled build with vcs_tag
('branch: None', 'vcs_tag: v1.0.0-rc', u'lifecycle: finished', 'outcome: canceled', u'status: canceled', 'stop_time: 2016-09-05T11:50:30.319Z')

# successful build with vcs_tag
('branch: None', 'vcs_tag: v1.0.0', u'lifecycle: finished', 'outcome: success', u'status: success', 'stop_time: 2016-09-05T11:56:10.305Z')