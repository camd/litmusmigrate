select tc.testcase_id, tc.summary, tc.details, tc.regression_bug_id, 
  tc.community_enabled, tc.steps, tc.expected_results,
  u.email, sg.name as sg_name, tg.name as tg_name
from testcases AS tc
left join branches AS b on b.branch_id = tc.branch_id
left join users AS u on tc.author_id = u.user_id
left join testcase_subgroups AS sg_map on tc.testcase_id = sg_map.testcase_id
left join subgroups AS sg on sg_map.subgroup_id = sg.subgroup_id
left join subgroup_testgroups AS tg_map on sg.subgroup_id = tg_map.subgroup_id
left join testgroups AS tg on tg_map.testgroup_id = tg.testgroup_id
where b.name = '3.0 Branch'
;