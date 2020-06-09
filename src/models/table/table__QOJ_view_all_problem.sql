CREATE OR REPLACE VIEW v_all_problem AS (SELECT QP_QPG_QUC_QU.*, QUP.up_state, QUP.up_query FROM QOJ_user_problem AS QUP RIGHT JOIN 	
    (SELECT QP_QPG.*, QUC_QU.user_id, QUC_QU.user_name, QUC_QU.uc_type FROM 
		(SELECT QP.p_id, QP.p_title, QP.p_content, QPG.* FROM QOJ_problem AS QP LEFT JOIN 
			(SELECT pg_id, pg_title, pg_activate, class_id FROM QOJ_problem_group) AS QPG ON QP.pg_id = QPG.pg_id) AS QP_QPG INNER JOIN 
				(SELECT QUC.*, QU.user_name FROM QOJ_user_class AS QUC LEFT JOIN 
					(SELECT user_id, user_name FROM QOJ_user) AS QU ON QUC.user_id = QU.user_id) AS QUC_QU ON QP_QPG.class_id = QUC_QU.class_id) AS QP_QPG_QUC_QU ON QP_QPG_QUC_QU.p_id = QUP.p_id AND QP_QPG_QUC_QU.user_id = QUP.user_id);
