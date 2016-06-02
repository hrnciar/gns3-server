#!/usr/bin/env python
#
# Copyright (C) 2016 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tests.utils import asyncio_patch


def test_compute_create_without_id(http_controller, controller):

    params = {
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params, example=True)
    assert response.status == 201
    assert response.route == "/computes"
    assert response.json["user"] == "julien"
    assert response.json["compute_id"] is not None
    assert "password" not in response.json

    assert len(controller.computes) == 1
    assert controller.computes[response.json["compute_id"]].host == "example.com"


def test_compute_create_with_id(http_controller, controller):

    params = {
        "compute_id": "my_compute_id",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params, example=True)
    assert response.status == 201
    assert response.route == "/computes"
    assert response.json["user"] == "julien"
    assert "password" not in response.json

    assert len(controller.computes) == 1
    assert controller.computes["my_compute_id"].host == "example.com"


def test_compute_get(http_controller, controller):

    params = {
        "compute_id": "my_compute/id",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201

    response = http_controller.get("/computes/my_compute/id", example=True)
    assert response.status == 200
    assert response.json["protocol"] == "http"


def test_compute_update(http_controller, controller):

    params = {
        "compute_id": "my_compute/id",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201

    response = http_controller.get("/computes/my_compute/id")
    assert response.status == 200
    assert response.json["protocol"] == "http"

    params["protocol"] = "https"
    response = http_controller.put("/computes/my_compute/id", params, example=True)

    assert response.status == 200
    assert response.json["protocol"] == "https"


def test_compute_list(http_controller, controller):

    params = {
        "compute_id": "my_compute_id",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure",
        "name": "My super server"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201
    assert response.route == "/computes"
    assert response.json["user"] == "julien"
    assert "password" not in response.json

    response = http_controller.get("/computes", example=True)
    assert response.json == [
        {
            'compute_id': 'my_compute_id',
            'connected': False,
            'host': 'example.com',
            'port': 84,
            'protocol': 'http',
            'user': 'julien',
            'name': 'My super server'

        }
    ]


def test_compute_delete(http_controller, controller):

    params = {
        "compute_id": "my_compute/id",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201

    response = http_controller.get("/computes")
    assert len(response.json) == 1

    response = http_controller.delete("/computes/my_compute/id")
    assert response.status == 204

    response = http_controller.get("/computes")
    assert len(response.json) == 0


def test_compute_list_images(http_controller, controller):

    params = {
        "compute_id": "my_compute",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201

    with asyncio_patch("gns3server.controller.compute.Compute.forward", return_value=[]) as mock:
        response = http_controller.get("/computes/my_compute/qemu/images")
        assert response.json == []
        mock.assert_called_with("qemu", "images")


def test_compute_list_vms(http_controller, controller):

    params = {
        "compute_id": "my_compute",
        "protocol": "http",
        "host": "example.com",
        "port": 84,
        "user": "julien",
        "password": "secure"
    }
    response = http_controller.post("/computes", params)
    assert response.status == 201

    with asyncio_patch("gns3server.controller.compute.Compute.forward", return_value=[]) as mock:
        response = http_controller.get("/computes/my_compute/virtualbox/vms")
        assert response.json == []
        mock.assert_called_with("virtualbox", "vms")
