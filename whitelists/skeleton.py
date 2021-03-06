from whitelists.base import whitelist

"""@skeleton docstring
The skeleton dataset is the lightest weight of all images.

  * fully sanitized
  * heavily trimmed

It is suitable for work on:

  * the unbranded D.o theme
  * case studies
  * issue queue

It is NOT suitable for work on:

  * D.o brand elements
  * commit logs
  * git
  * packaging
  * solr

Notes:

If you are working with the following functionality, you are expected to create your own test data. Production values are NOT included in this dump.

  * Issue subscriptions (flag_content / flag_count)
  * Multiple e-mail address (multiple_email)
  * Tracker (tracker_node)
  * User Profiles (profile_value)

"""
whitelist.update(
    table="users",
    columns=[
        "_sanitize_timestamp:access",
    ])

whitelist.update(
    table="users_access",
    columns=[
        "_sanitize_timestamp:access",
    ])

whitelist.set_handler(
    table="apachesolr_index_entities",
    handler="nodata"
)

whitelist.set_handler(
    table="apachesolr_index_entities_node",
    handler="nodata"
)

whitelist.set_handler(
  table="flag_content",
  handler="nodata"
)

whitelist.set_handler(
  table="flag_counts"
  handler="nodata"
)

whitelist.set_handler(
  table="tracker_node",
  handler="nodata"
)

whitelist.set_handler(
  table="profile_value",
  handler="nodata"
)

whitelist.set_handler(
  table="search_api*",
  handler="nodata"
)

whitelist.set_handler(
  table="versioncontrol*"
  handler="nodata"
)

whitelist.set_handler(
  table="drupalorg_git_push*"
  handler="nodata"
)

whitelist.set_handler(
  table="httpbl"
  handler="nodata"
)

whitelist.set_handler(
  table="role_activity"
  handler="nodata"
)

# Trim the image to selected projects

whitelist.set_handler(
  table="field_data*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="field_revision*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="sampler_project*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="sampler_sampler*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="project_usage*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="pift*"
  handler="select_by_project"
)

whitelist.set_handler(
  table="taxonomy_index"
  handler="select_by_project"
)

# Original queries to limit the size of the dataset

cleanup = """
  -- Get rid of unpublished/blocked nodes, users, comments and related data in other tables.
  DELETE f FROM field_data_body AS f INNER JOIN node n ON (f.entity_id = n.nid AND f.entity_type = 'node' AND n.status <> 1);
  DELETE f FROM field_revision_body AS f INNER JOIN node n ON (f.entity_id = n.nid AND f.entity_type = 'node' AND n.status <> 1);
  DELETE f FROM field_data_comment_body AS f INNER JOIN node n ON (f.entity_id = n.nid AND f.entity_type = 'node' AND n.status <> 1);
  DELETE f FROM field_revision_comment_body AS f INNER JOIN node n ON (f.entity_id = n.nid AND f.entity_type = 'node' AND n.status <> 1);

  -- Get rid of unpublished/blocked nodes, users, comments and related data in other tables.
  DELETE FROM node WHERE status <> 1;
  DELETE FROM comment WHERE status <> 1;
  DELETE node FROM node LEFT JOIN users ON node.uid = users.uid WHERE users.uid IS NULL;
  DELETE node_revision FROM node_revision LEFT JOIN node ON node.nid = node_revision.nid WHERE node.nid IS NULL;
  DELETE comment FROM comment LEFT JOIN node ON node.nid = comment.nid WHERE node.nid IS NULL;
  DELETE comment FROM comment LEFT JOIN users ON comment.uid = users.uid WHERE users.uid IS NULL;
  DELETE comment FROM comment LEFT JOIN comment c2 ON comment.pid = c2.cid WHERE c2.cid IS NULL AND comment.pid <> 0;
  DELETE files FROM files LEFT JOIN users ON files.uid = users.uid WHERE users.uid IS NULL;
  DELETE file_managed FROM file_managed LEFT JOIN users ON file_managed.uid = users.uid WHERE users.uid IS NULL;
  DELETE image FROM image LEFT JOIN node ON image.nid = node.nid WHERE node.nid IS NULL;

# http://drupalcode.org/project/infrastructure.git/blob/HEAD:/snapshot/drupal.reduce.sql

  -- CAUTION: DO NOT RUN THIS ON DATABASE WHERE YOU CARE ABOUT THE INFORMATION!!!

  -- Reduce the DB size to make development easier.
  -- http://drupal.org/node/636340#comment-3193836
  DELETE FROM node WHERE type IN ('forum','project_issue') AND created < (unix_timestamp() - 60*24*60*60);
  DELETE node FROM node LEFT JOIN comment ON node.nid = comment.nid WHERE node.type = 'forum' AND comment.nid IS NULL;
  DELETE tracker_user FROM tracker_user LEFT JOIN node ON tracker_user.nid = node.nid WHERE node.nid IS NULL;
  DELETE tracker_user FROM tracker_user LEFT JOIN users ON tracker_user.uid = users.uid WHERE users.uid IS NULL;
  DELETE node_revision FROM node_revision LEFT JOIN node ON node.nid = node_revision.nid WHERE node.nid IS NULL;
  DELETE node_revision FROM node_revision LEFT JOIN node ON node.nid = node_revision.nid AND node.vid = node_revision.vid WHERE node.nid IS NULL AND node_revision.timestamp < (unix_timestamp() - 60*24*60*60);
  DELETE node_comment_statistics FROM node_comment_statistics LEFT JOIN node ON node.nid = node_comment_statistics.nid WHERE node.nid IS NULL;
  DELETE comment FROM comment LEFT JOIN node ON node.nid = comment.nid WHERE node.nid IS NULL;

  DELETE field_data_body FROM field_data_body LEFT JOIN node_revision ON node_revision.vid = field_data_body.revision_id WHERE node_revision.vid IS NULL;
  DELETE field_revision_body FROM field_revision_body LEFT JOIN node_revision ON node_revision.vid = field_revision_body.revision_id WHERE node_revision.vid IS NULL;
  DELETE field_data_comment_body FROM field_data_comment_body LEFT JOIN comment ON comment.cid = field_data_comment_body.entity_id WHERE comment.cid IS NULL;
  DELETE field_data_field_issue_changes FROM field_data_field_issue_changes LEFT JOIN comment ON comment.cid = field_data_field_issue_changes.entity_id WHERE comment.cid IS NULL;
  DELETE field_revision_field_issue_changes FROM field_revision_field_issue_changes LEFT JOIN field_data_field_issue_changes ON field_data_field_issue_changes.entity_id = field_revision_field_issue_changes.entity_id WHERE field_data_field_issue_changes.entity_id IS NULL;
  DELETE field_revision_field_issue_files FROM field_revision_field_issue_files LEFT JOIN node_revision ON node_revision.vid = field_revision_field_issue_files.revision_id WHERE node_revision.vid IS NULL;

  DELETE FROM versioncontrol_operations WHERE author_date < (unix_timestamp() - 60*24*60*60);
  DELETE versioncontrol_item_revisions FROM versioncontrol_item_revisions LEFT JOIN versioncontrol_operations ON versioncontrol_item_revisions.vc_op_id = versioncontrol_operations.vc_op_id WHERE versioncontrol_operations.vc_op_id IS NULL;
  DELETE versioncontrol_git_item_revisions FROM versioncontrol_git_item_revisions LEFT JOIN versioncontrol_item_revisions ON versioncontrol_git_item_revisions.item_revision_id = versioncontrol_item_revisions.item_revision_id WHERE versioncontrol_item_revisions.item_revision_id IS NULL;
  DELETE v FROM search_api_db_project_issues_comments_comment_body_value v LEFT JOIN node n ON n.nid = v.item_id WHERE n.nid IS NULL;
  DELETE v FROM search_api_db_project_issues_body_value v LEFT JOIN node n ON n.nid = v.item_id WHERE n.nid IS NULL;
  DELETE v FROM search_api_db_project_issues v LEFT JOIN node n ON n.nid = v.item_id WHERE n.nid IS NULL
""".split(';')
