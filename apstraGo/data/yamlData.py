{
    'apstrago': {
        'required': True,
        'type': 'dict',
        'allowed': ['login', 'resourcePools', 'blueprints', 'devices', 'racks', 'templates'],
        'schema': { 
            'login': {
                'required': True,
                'type': 'dict',
                'schema': { 
                    'username': {
                        'required': True,
                        'type': 'string',
                        'empty': False
                    },
                    'password': {
                        'required': True,
                        'type': 'string',
                        'empty': False
                    },
                    'address': {
                        'required': True,
                        'type': 'string',
                        'empty': False
                    },
                    'port': {
                        
                        'type': 'string'
                    }
                }
            },
            'resourcePools': {
                'type': 'dict',
                'allowed': ['asnPools', 'ipPools', 'vniPools'],
                'schema': {
                    'asnPools': {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'contains': ['poolName', 'firstASN', 'lastASN'],
                            'schema': {
                                'poolName': {
                                    'type': 'string',
                                    'empty': False
                                },
                                'firstASN': {
                                    'type': 'string',
                                    'empty': False
                                },
                                'lastASN': {
                                    'type': 'string',
                                    'empty': False
                                }
                            }
                        }   
                    },
                    'ipPools': {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'contains': ['poolName', 'network'],
                            'schema': {
                                'poolName': {
                                    'type': 'string',
                                    'empty': False
                                },
                                'network': {
                                    'type': 'string',
                                    'empty': False
                                }
                            }
                        }   
                    },
                    'vniPools': {
                        'type': 'list',
                        'schema': {
                            'type': 'dict',
                            'contains': ['poolName', 'firstVNI', 'lastVNI'],
                            'schema': {
                                'poolName': {
                                    'type': 'string',
                                    'empty': False
                                },
                                'firstVNI': {
                                    'type': 'string',
                                    'empty': False
                                },
                                'lastVNI': {
                                    'type': 'string',
                                    'empty': False
                                }
                            }
                        }   
                    }
                }  
            },
            'blueprints': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'contains': ['name', 'templateName'],
                    'schema': {
                        'name': {
                            'type': 'string',
                            'empty': False
                        },
                        'templateName': {
                            'type': 'string',
                            'empty': False
                        }
                    }
                }   
            },
            'devices': {
                'type': 'dict',
                'contains': ['username', 'password', 'platform', 'addresses'],
                'schema': { 
                    'username': {
                        'type': 'string',
                        'empty': False
                    },
                    'password': {
                        'type': 'string',
                        'empty': False
                    },
                    'platform': {
                        'type': 'string',
                        'empty': False
                    },
                    'agentType': {
                        'type': 'string',
                        'empty': False
                    },
                    'operationMode': {
                        'type': 'string',
                        'empty': False
                    },
                    'acknowledge': {
                        'type': 'boolean',
                        'empty': False
                    },
                    'addresses': {
                        'type': 'list',
                        'empty': False,
                        'schema': {
                            'type': 'string',
                            'empty': False
                        }
                    }
                }
            },
            'racks': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'contains': ['rackName'],
                    'schema': {
                        'rackName': {
                            'type': 'string',
                            'empty': False
                        },
                        'rackTypeDesc': {
                            'type': 'string',
                            'empty': False
                        },
                        'connectivityType': {
                            'type': 'string',
                            'empty': False
                        },
                        'leafName': {
                            'type': 'string',
                            'empty': False
                        },
                        'linksPerSpine': {
                            'type': 'string',
                            'empty': False
                        },
                        'leafLogicalDevice': {
                            'type': 'string',
                            'empty': False
                        },
                        'leafSpineLinkSpeedUnit': {
                            'type': 'string',
                            'empty': False
                        },
                        'leafSpineLinkSpeedValue': {
                            'type': 'string',
                            'empty': False
                        },
                        'serverName': {
                            'type': 'string',
                            'empty': False
                        },
                        'serverCount': {
                            'type': 'string',
                            'empty': False
                        },
                        'serverLogicalDevice': {
                            'type': 'string',
                            'empty': False
                        },
                        'leafServerLinkName': {
                            'type': 'string',
                            'empty': False
                        },
                        'lagType': {
                            'type': 'string',
                            'empty': False
                        },
                        'LeafServerLinkSpeedUnit': {
                            'type': 'string',
                            'empty': False
                        },
                        'LeafServerLinkSpeedValue': {
                            'type': 'string',
                            'empty': False
                        },
                        'linksPerLeafCount': {
                            'type': 'string',
                            'empty': False
                        },
                    }
                }   
            },
            'templates': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'contains': ['templateName'],
                    'schema': {
                        'templateName': {
                            'type': 'string',
                            'empty': False
                        },
                        'spineLogicalDeviceId': {
                            'type': 'string',
                            'empty': False
                        },
                        'rackTypeList': {
                            'type': 'list',
                            'empty': False,
                            'schema': {
                                'type': 'string',
                                'empty': False
                            }
                        },
                        'spineCount': {
                            'type': 'string',
                            'empty': False
                        },
                        'ipChoice': {
                            'type': 'string',
                            'empty': False
                        },
                        'asnAllocation': {
                            'type': 'string',
                            'empty': False
                        },
                        'overlayControl': {
                            'type': 'string',
                            'empty': False
                        }
                    }
                }   
            }
        }
    }
}