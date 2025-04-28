create database hpha;
use hpha;

-- Common tables

-- Purpose: Create a table to store the users.
create table users (
    id bigint unsigned auto_increment primary key,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    username varchar(255),
    email varchar(255) not null,
    password varchar(255) not null,
    is_sys_admin tinyint(1) not null default 0,
    last_login timestamp,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_users (email)
);

-- Purpose: Create a table to store the departments.
create table departments (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    code varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_departments (name, code)
);

-- Purpose: Create a table to store the roles.
create table roles (
    id bigint unsigned primary key,
    name varchar(255) not null,
    unique key unique_roles (name)
);

insert into roles (id, name) values
    (1, 'Administrator'),
    (2, 'Initiator'),
    (3, 'Delegate'),
    (4, 'Supervisor'),
    (5, 'Manager'),
    (6, 'Director'),
    (7, 'VP for Department'),
    (8, 'VP / CFE'),
    (9, 'CEO'),
    (10, 'Board Chair');

-- Purpose: Create a table to store the users and their roles in the departments.
create table departments_users_roles (
    id bigint unsigned auto_increment primary key,
    department_id bigint unsigned not null,
    user_id bigint unsigned not null,
    role_id bigint unsigned not null,
    foreign key (department_id) references departments(id),
    foreign key (user_id) references users(id),
    foreign key (role_id) references roles(id),
    unique key unique_departments_users_roles (department_id, user_id, role_id)
);

-- Purpose: Create a table to store the sites.
create table sites (
    id bigint unsigned auto_increment primary key,
    name varchar(100) not null,
    mnemonic varchar(20) not null,
    location varchar(60) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_sites (mnemonic)
);

insert into sites (name, mnemonic, location) values
    ('Stratford General Hospital', 'SGH', 'Stratford'),
    ('Seaforth Community Hospital', 'SEA', 'Seaforth'),
    ('Alexandra & Marine General Hospital', 'AMGH', 'Goderich'),
    ('St. Marys Memorial Hospital', 'SMMH', 'St. Marys'),
    ('Clinton Public Hospital', 'CPH', 'Clinton');

-- Purpose: Create a table to store the flows for the requisition approvals.
create table flows (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_flows (name)
);

-- Purpose: Create a table to store flow versions
create table flow_versions (
    id bigint unsigned auto_increment primary key,
    flow_id bigint unsigned not null,
    version int not null,
    is_active tinyint(1) not null default 1,
    effective_from timestamp not null default current_timestamp,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (flow_id) references flows(id),
    unique key unique_flow_versions (flow_id, version)
);

-- Purpose: Create a table to store the flow approval rules with versions
create table flow_approval_rules (
    id bigint unsigned auto_increment primary key,
    flow_version_id bigint unsigned not null,
    role_id bigint unsigned not null,
    approval_level int not null,
    min_amount decimal(15, 2) not null,
    max_amount decimal(15, 2) not null,
    can_skip tinyint(1) not null default 0,
    skip_reason_required tinyint(1) not null default 1,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (flow_version_id) references flow_versions(id),
    foreign key (role_id) references roles(id),
    unique key unique_flow_approval_rules (flow_version_id, approval_level)
);

-- Purpose: Create a table to store requisition types
create table requisition_types (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    code varchar(50) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_requisition_types (code)
);

insert into requisition_types (name, code) values
    ('Purchase Requisition', 'PR'),
    ('Personal Expense', 'PE'),
    ('Travel Expense', 'TE');

-- Purpose: Create a table to store the flow status.
create table requisition_status (
    id bigint unsigned primary key,
    name varchar(255) not null,
    unique key unique_requisition_status (name)
);

insert into requisition_status (id, name) values
    (1, 'Draft'),
    (2, 'In Progress'),
    (3, 'Pending'),
    (4, 'Approved'),
    (5, 'Rejected'),
    (6, 'Cancelled'),
    (7, 'Skipped');

-- Purpose: Create a generic requisitions table
create table requisitions (
    id bigint unsigned auto_increment primary key,
    requisition_number varchar(50) not null,
    requisition_type_id bigint unsigned not null,
    flow_id bigint unsigned not null,
    flow_version_id bigint unsigned not null,
    department_id bigint unsigned not null,
    initiator_id bigint unsigned not null,
    current_status_id bigint unsigned not null,
    total_amount decimal(15, 2) not null,
    submission_date timestamp,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    foreign key (requisition_type_id) references requisition_types(id),
    foreign key (flow_id) references flows(id),
    foreign key (flow_version_id) references flow_versions(id),
    foreign key (department_id) references departments(id),
    foreign key (initiator_id) references users(id),
    foreign key (current_status_id) references requisition_status(id),
    unique key unique_requisitions (requisition_number)
);

-- Purpose: Create a table to track the approval workflow
create table requisition_approvals (
    id bigint unsigned auto_increment primary key,
    requisition_id bigint unsigned not null,
    approval_level int not null,
    role_id bigint unsigned not null,
    approver_id bigint unsigned null,
    status_id bigint unsigned not null,
    comments text,
    decision_date timestamp null,
    skipped tinyint(1) not null default 0,
    skip_reason varchar(500),
    skipped_by_user_id bigint unsigned null,
    skipped_at timestamp null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (requisition_id) references requisitions(id),
    foreign key (role_id) references roles(id),
    foreign key (approver_id) references users(id),
    foreign key (status_id) references requisition_status(id),
    foreign key (skipped_by_user_id) references users(id),
);

-- Purchase Requisition Specific Tables

-- Purpose: Create a table to store the purchase requisition types.
create table purchase_requisition_types (
    id bigint unsigned auto_increment primary key,
    name varchar(255) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    deleted_at timestamp,
    unique key unique_purchase_requisition_types (name)
);

insert into purchase_requisition_types (name) values
    ('Expense'),
    ('Capital'),
    ('Construction');

-- Purpose: Create a table to store the purchase requisitions (specialized from requisitions).
create table purchase_requisition_details (
    id bigint unsigned auto_increment primary key,
    requisition_id bigint unsigned not null,
    site_id bigint unsigned not null,
    purchase_type_id bigint unsigned not null,
    po_number varchar(20),
    tel_ext varchar(20),
    comments varchar(5000),
    suggested_supplier varchar(200),
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (requisition_id) references requisitions(id),
    foreign key (site_id) references sites(id),
    foreign key (purchase_type_id) references purchase_requisition_types(id),
    unique key unique_purchase_requisition_details (requisition_id)
);

-- Purpose: Create a table to store the purchase requisition items.
create table purchase_requisition_items (
    id bigint unsigned auto_increment primary key,
    purchase_requisition_detail_id bigint unsigned not null,
    quantity int not null,
    unit_measure varchar(20) not null,
    unit_price decimal(10, 2) not null,
    vendor_catalogue_number varchar(20) not null,
    eoc_cip varchar(20) not null,
    description varchar(5000) not null,
    total decimal(10, 2) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (purchase_requisition_detail_id) references purchase_requisition_details(id)
);

-- Personal Expense Reimbursement Specific Tables

-- Purpose: Create a table for personal expense requisition details
create table personal_expense_details (
    id bigint unsigned auto_increment primary key,
    requisition_id bigint unsigned not null,
    expense_date date not null,
    expense_type varchar(100) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (requisition_id) references requisitions(id),
    unique key unique_personal_expense_details (requisition_id)
);

-- Travel Expense Reimbursement Specific Tables

-- Purpose: Create a table for travel expense requisition details
create table travel_expense_details (
    id bigint unsigned auto_increment primary key,
    requisition_id bigint unsigned not null,
    travel_start_date date not null,
    travel_end_date date not null,
    destination varchar(200) not null,
    purpose varchar(500) not null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp on update current_timestamp,
    foreign key (requisition_id) references requisitions(id),
    unique key unique_travel_expense_details (requisition_id)
);

-- Insert default flow types
insert into flows (name) values
    ('Purchase Requisition - Expense'),
    ('Purchase Requisition - Capital'),
    ('Purchase Requisition - Construction'),
    ('Personal Expense Reimbursement'),
    ('Travel Expense Reimbursement');

-- Add initial flow versions
insert into flow_versions (flow_id, version, is_active, effective_from)
select id, 1, 1, current_timestamp from flows;

-- Add approval rules for each flow version
-- Example for Purchase Requisition - Expense
insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    3, 1, 0.00, 999.99;  -- Delegate up to $999.99

insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    5, 2, 1000.00, 4999.99;  -- Manager $1,000 to $4,999.99

insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    6, 3, 5000.00, 24999.99;  -- Director $5,000 to $24,999.99

insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    7, 4, 25000.00, 99999.99;  -- VP for Department $25,000 to $99,999.99

insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    8, 5, 100000.00, 499999.99;  -- VP/CFE $100,000 to $499,999.99

insert into flow_approval_rules (flow_version_id, role_id, approval_level, min_amount, max_amount)
select 
    (select id from flow_versions where flow_id = (select id from flows where name = 'Purchase Requisition - Expense') and version = 1),
    9, 6, 500000.00, 9999999999.99;  -- CEO $500,000 and above
