# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from nailgun.api.models import Cluster
from nailgun.api.models import Node
from nailgun.db import db
from nailgun.orchestrator.provisioning_serializers import serialize
from nailgun.test.base import BaseIntegrationTest


class TestProvisioningSerializer(BaseIntegrationTest):

    def test_ubuntu_serializer(self):
        release = self.env.create_release(
            api=False, operating_system='Ubuntu')

        cluster = self.env.create(
            cluster_kwargs={
                'mode': 'multinode',
                'release': release.id},
            nodes_kwargs=[
                {'roles': ['controller'], 'pending_addition': True},
                {'roles': ['compute'], 'pending_addition': True}])

        cluster_db = self.db.query(Cluster).get(cluster['id'])
        serialized_cluster = serialize(cluster_db)

        for node in serialized_cluster['nodes']:
            node_db = db().query(Node).filter_by(fqdn=node['hostname']).first()
            self.assertEquals(
                node['kernel_options']['netcfg/choose_interface'],
                node_db.admin_interface.name)
