#!/usr/bin/env python
# encoding: utf-8
"""
populate_ccm_cache.py

Created by Aske Olsson on 2011-05-13.
Copyright (c) 2011, Nokia
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of the Nokia nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.    IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from CCMHistory import get_project_chain
from SynergySession import SynergySession
from SynergySessions import SynergySessions
import ccm_cache
import ccm_objects_in_project
from load_configuration import load_config_file
import logging as logger


def update_project_with_members(project, ccm, ccmpool):
    print "Loading object %s" % project
    project_obj = ccm_cache.get_object(project, ccm=ccm)
    if not project_obj.members:
        objects_in_project = ccm_objects_in_project.get_objects_in_project(project, ccm=ccm, ccmpool=ccmpool)
        project_obj.set_members(objects_in_project)
        ccm_cache.force_cache_update_for_object(project_obj)


def populate_cache_with_projects(config):
    heads = []
    if config.has_key('heads'):
        heads = config['heads']
    heads.append(config['master'])
    base_project = config['base_project']
    ccm, ccmpool = start_sessions(config)

    projects = []
    for head in heads:
        projects.extend(get_project_chain(head, base_project, ccm))

    # Got all the project chains - now get all the objects
    print sorted(set(projects))
    for project in sorted(set(projects)):
        populate_cache_with_objects_from_project(project, ccm, ccmpool)
#        update_project_with_members(project, ccm, ccmpool)

def populate_cache_with_project_and_members(project, ccm, ccmpool):
    print "Loading object %s" % project
    project_obj = ccm_cache.get_object(project, ccm=ccm)
    #assuming no project.members
    objects_in_project = ccm_objects_in_project.get_objects_in_project(project, ccm=ccm, ccmpool=ccmpool, use_cache=True)
    project_obj.set_members(objects_in_project)
    ccm_cache.force_cache_update_for_object(project_obj)


def populate_cache_with_objects_from_project(project, ccm, ccmpool):
    print "processing project %s" %project
    #first try to get the object from cache
    project_obj = ccm_cache.get_object(project, ccm)
    if not project_obj.members:
        populate_cache_with_project_and_members(project, ccm, ccmpool)

def start_sessions(config):
    ccm = SynergySession(server=config['server'], database=config['database'])
    ccm_pool = SynergySessions(server=config['server'], database=config['database'], nr_sessions=config['max_sessions'])
    return ccm, ccm_pool

def main():

    logger.basicConfig(filename='populate.log',level=logger.DEBUG)
    config = load_config_file()
    populate_cache_with_projects(config)


if __name__ == '__main__':
    main()
