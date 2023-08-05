"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
The MIT License

Copyright (c) 2020 Temporal Technologies Inc.  All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _ScheduleOverlapPolicy:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _ScheduleOverlapPolicyEnumTypeWrapper(
    google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[
        _ScheduleOverlapPolicy.ValueType
    ],
    builtins.type,
):  # noqa: F821
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    SCHEDULE_OVERLAP_POLICY_UNSPECIFIED: _ScheduleOverlapPolicy.ValueType  # 0
    SCHEDULE_OVERLAP_POLICY_SKIP: _ScheduleOverlapPolicy.ValueType  # 1
    """SCHEDULE_OVERLAP_POLICY_SKIP (default) means don't start anything. When the
    workflow completes, the next scheduled event after that time will be considered.
    """
    SCHEDULE_OVERLAP_POLICY_BUFFER_ONE: _ScheduleOverlapPolicy.ValueType  # 2
    """SCHEDULE_OVERLAP_POLICY_BUFFER_ONE means start the workflow again soon as the
    current one completes, but only buffer one start in this way. If another start is
    supposed to happen when the workflow is running, and one is already buffered, then
    only the first one will be started after the running workflow finishes.
    """
    SCHEDULE_OVERLAP_POLICY_BUFFER_ALL: _ScheduleOverlapPolicy.ValueType  # 3
    """SCHEDULE_OVERLAP_POLICY_BUFFER_ALL means buffer up any number of starts to all
    happen sequentially, immediately after the running workflow completes.
    """
    SCHEDULE_OVERLAP_POLICY_CANCEL_OTHER: _ScheduleOverlapPolicy.ValueType  # 4
    """SCHEDULE_OVERLAP_POLICY_CANCEL_OTHER means that if there is another workflow
    running, cancel it, and start the new one after the old one completes cancellation.
    """
    SCHEDULE_OVERLAP_POLICY_TERMINATE_OTHER: _ScheduleOverlapPolicy.ValueType  # 5
    """SCHEDULE_OVERLAP_POLICY_TERMINATE_OTHER means that if there is another workflow
    running, terminate it and start the new one immediately.
    """
    SCHEDULE_OVERLAP_POLICY_ALLOW_ALL: _ScheduleOverlapPolicy.ValueType  # 6
    """SCHEDULE_OVERLAP_POLICY_ALLOW_ALL means start any number of concurrent workflows.
    Note that with this policy, last completion result and last failure will not be
    available since workflows are not sequential.
    """

class ScheduleOverlapPolicy(
    _ScheduleOverlapPolicy, metaclass=_ScheduleOverlapPolicyEnumTypeWrapper
):
    """ScheduleOverlapPolicy controls what happens when a workflow would be started
    by a schedule, and is already running.
    """

SCHEDULE_OVERLAP_POLICY_UNSPECIFIED: ScheduleOverlapPolicy.ValueType  # 0
SCHEDULE_OVERLAP_POLICY_SKIP: ScheduleOverlapPolicy.ValueType  # 1
"""SCHEDULE_OVERLAP_POLICY_SKIP (default) means don't start anything. When the
workflow completes, the next scheduled event after that time will be considered.
"""
SCHEDULE_OVERLAP_POLICY_BUFFER_ONE: ScheduleOverlapPolicy.ValueType  # 2
"""SCHEDULE_OVERLAP_POLICY_BUFFER_ONE means start the workflow again soon as the
current one completes, but only buffer one start in this way. If another start is
supposed to happen when the workflow is running, and one is already buffered, then
only the first one will be started after the running workflow finishes.
"""
SCHEDULE_OVERLAP_POLICY_BUFFER_ALL: ScheduleOverlapPolicy.ValueType  # 3
"""SCHEDULE_OVERLAP_POLICY_BUFFER_ALL means buffer up any number of starts to all
happen sequentially, immediately after the running workflow completes.
"""
SCHEDULE_OVERLAP_POLICY_CANCEL_OTHER: ScheduleOverlapPolicy.ValueType  # 4
"""SCHEDULE_OVERLAP_POLICY_CANCEL_OTHER means that if there is another workflow
running, cancel it, and start the new one after the old one completes cancellation.
"""
SCHEDULE_OVERLAP_POLICY_TERMINATE_OTHER: ScheduleOverlapPolicy.ValueType  # 5
"""SCHEDULE_OVERLAP_POLICY_TERMINATE_OTHER means that if there is another workflow
running, terminate it and start the new one immediately.
"""
SCHEDULE_OVERLAP_POLICY_ALLOW_ALL: ScheduleOverlapPolicy.ValueType  # 6
"""SCHEDULE_OVERLAP_POLICY_ALLOW_ALL means start any number of concurrent workflows.
Note that with this policy, last completion result and last failure will not be
available since workflows are not sequential.
"""
global___ScheduleOverlapPolicy = ScheduleOverlapPolicy
