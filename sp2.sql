--ALREADY HAVE:
    --INSTRUCTOR CRUD
    --STUDENT CRUD
    --SECTION CRUD
    --ENROLL IN SECTION (STUDENT)
    --ASSIGN TEACHER (SECTION)
    --DROP SECTION (STUDENT)
    --GIVE GRADE TO STUDENT (FROM TEACHER, IN SECTION)

--STILL NEED:
    --ADMIN
        --CRUD COURSE
        --CRUD CLASSROOM
        --CRUD DEPARTMENT
        --CRUD TIME SLOT
        --MODIDY/REMOVE TEACHER TO CLASS
    --INSTRUCTOR
        --CHANGE GRADES
        --ADD/REMOVE STUDENT AS ADVISOR
        --MODIFY COURSE PREREQS
        --REMOVE STUDENT FROM SECTION (KIND OF JUST DROP)
        --CHECK SECTION ROSTER
        --CHECK WHICH SECTIONS THEY ARE TEACHING
        --MODIFY PERSONAL INFO
    --STUDENT
        --CHECK FINAL GRADES
        --CHECK COURSES BASED ON SEMESTER
        --CHECK SECTION INFO
        --CHECK ADVISOR INFO
        --MODIFY PERSONAL INFO
    --EXTRA
        --GET AVERAGE GRADE OF ALL STUDENTS IN DEPARTMENT
        --GET AVERAGE GRADE OF A CLASS ACROSS RANGE OF SEMESTERS
        --SHOW TOTAL STUDENTS (PAST AND CURRENT) BY DEPARTMENT
        --SHOW CURRENT STUDENTS BY DEPARTMENT

--CRUD COURSE

DELIMITER //
CREATE PROCEDURE createCourse (
    IN pc_id VARCHAR(8),
    IN pTitle VARCHAR(50),
    IN pDept_name VARCHAR(20),
    IN pCred NUMERIC(2,0)
)
BEGIN
    INSERT INTO course (course_id, title, dept_name, credits)
    VALUES (pc_id, pTitle, pDept_name, pCred);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE findCourse (
IN pc_id VARCHAR(8),
)
BEGIN
    SELECT * FROM course
    WHERE course.course_id = pc_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateCourse (
    IN pc_id VARCHAR(8),
    IN pTitle VARCHAR(50),
    IN pDept_name VARCHAR(20),
    IN pCred NUMERIC(2,0)
)
BEGIN
    IF pTitle IS NOT NULL AND pTitle <> '' THEN
        UPDATE course
        SET title = pTitle
        WHERE course.course_id = pc_id;
    END IF;
    IF pDept_name IS NOT NULL AND pDept_name <> '' THEN
        UPDATE course
        SET dept_name = pDept_name
        WHERE course.course_id = pc_id;
    END IF;
    IF pCred IS NOT NULL AND pCred <> '' THEN
        UPDATE course
        SET credits = pCred
        WHERE course.course_id = pc_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteCourse (
    In pCourse_id VARCHAR(8)
)
BEGIN
    delete from section
    where section.course_id = pCourse_id;
    delete from course
    where course.course_id = pCourse_id;
END //
DELIMITER ;


--CRUD CLASSROOM

DELIMITER //
CREATE PROCEDURE createClassroom (
    IN pRoom_id VARCHAR(5),
    IN pBuilding VARCHAR(15),
    IN pRoom_number VARCHAR(7),
    IN pCapacity NUMERIC(4,0)
)
BEGIN
    INSERT INTO classroom (room_id, building, room_number, capacity)
    VALUES (pRoom_id, pBUilding, pRoom_number, pCapacity);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE findClassroom (
IN pRoom_id VARCHAR(8),
)
BEGIN
    SELECT * FROM classroom
    WHERE classroom.room_id = pRoom_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateClassroom (
    IN pRoom_id VARCHAR(5),
    IN pBuilding VARCHAR(15),
    IN pRoom_number VARCHAR(7),
    IN pCapacity NUMERIC(4,0)
)
BEGIN
    IF pBuilding IS NOT NULL AND pBuilding <> '' THEN
        UPDATE classroom
        SET building = pBuilding
        WHERE classroom.room_id = pRoom_id;
    END IF;
    IF pRoom_number IS NOT NULL AND pRoom_number <> '' THEN
        UPDATE classroom
        SET room_number = pRoom_number
        WHERE classroom.room_id = pRoom_id;
    END IF;
    IF pCapacity IS NOT NULL AND pCapacity <> '' THEN
        UPDATE classroom
        SET capacity = pCapacity
        WHERE classroom.room_id = pRoom_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteClassroom (
    IN pRoom_id VARCHAR(5)
)
BEGIN
    delete from classroom
    where classroom.room_id = pRoom_id;
END //
DELIMITER ;


--CRUD DEPARTMENT

DELIMITER //
CREATE PROCEDURE createDept (
    IN pDept_name varchar(20), 
	IN pBuilding varchar(15), 
	IN pBudget numeric(12,2)
)
BEGIN
    INSERT INTO department (dept_name, building, budget)
    VALUES (pDept_name, pBuilding, pBudget);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE findDept (
IN pDept_name VARCHAR(20),
)
BEGIN
    SELECT * FROM department
    WHERE department.dept_name = pDept_name;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateDept (
    IN pDept_name varchar(20), 
	IN pBuilding varchar(15), 
	IN pBudget numeric(12,2)
)
BEGIN
    IF pBuilding IS NOT NULL AND pBuilding <> '' THEN
        UPDATE department
        SET building = pBuilding
        WHERE department.dept_name = pDept_name;
    END IF;
    IF pBudget IS NOT NULL AND pBudget <> '' THEN
        UPDATE department
        SET budget = pBudget
        WHERE department.dept_name = pDept_name;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteDept (
    IN pDept_name VARCHAR(20)
)
BEGIN
    delete from department
    where department.dept_name = pDept_name;
END //
DELIMITER ;


--CRUD TIME SLOT

DELIMITER //
CREATE PROCEDURE createTimeSlot (
    IN PTime_slot_id varchar(4),
	IN pDay varchar(1),
	IN pStart_hr	numeric(2),
	IN pStart_min numeric(2),
	IN pEnd_hr numeric(2),
	IN pEnd_min numeric(2)
)
BEGIN
    INSERT INTO time_slot (time_slot_id, day, start_hr, start_min, end_hr, end_min)
    VALUES (pTime_slot_id, pDay, pStart_hr, pStart_min, pEnd_hr, pEnd_min);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE findTimeSlot (
IN pTime_slot_id VARCHAR(4),
)
BEGIN
    SELECT * FROM time_slot
    WHERE time_slot.time_slot_id = pTime_slot_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateTimeSlot (
    IN PTime_slot_id varchar(4),
	IN pDay varchar(1),
	IN pStart_hr	numeric(2),
	IN pStart_min numeric(2),
	IN pEnd_hr numeric(2),
	IN pEnd_min numeric(2)
)
BEGIN
    IF pDay IS NOT NULL AND pDay <> '' THEN
        UPDATE time_slot
        SET day = pDay
        WHERE time_slot.time_slot_id = pTime_slot_id;
    END IF;
    IF pStart_hr IS NOT NULL AND pStart_hr <> '' THEN
        UPDATE time_slot
        SET start_hr = pStart_hr
        WHERE time_slot.time_slot_id = pTime_slot_id;
    END IF;
    IF pStart_min IS NOT NULL AND pStart_min <> '' THEN
        UPDATE time_slot
        SET start_min = pStart_min
        WHERE time_slot.time_slot_id = pTime_slot_id;
    END IF;
    IF pEnd_hr IS NOT NULL AND pEnd_hr <> '' THEN
        UPDATE time_slot
        SET end_hr = pEnd_hr
        WHERE time_slot.time_slot_id = pTime_slot_id;
    END IF;
    IF pEnd_min IS NOT NULL AND pEnd_min <> '' THEN
        UPDATE time_slot
        SET end_min = pEnd_min
        WHERE time_slot.time_slot_id = pTime_slot_id;
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE deleteTimeSlot (
    IN p_id VARCHAR(20)
)
BEGIN
    delete from time_slot
    where time_slot.time_slot_id = p_id;
END //
DELIMITER ;


--MODIDY/REMOVE TEACHER TO CLASS
DELIMITER //
CREATE PROCEDURE modifyTeacher (
    IN pInstructor_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8)
)
BEGIN
    UPDATE teaches
    SET ID = pInstructor_id
    WHERE teaches.course_id = pCourse_id
    AND teaches.sec_id = pSec_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE removeTeacher (
    IN pInstructor_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8)
)
BEGIN
    delete from teaches
    WHERE teaches.ID = pInstructor_id
    AND teaches.course_id = pCourse_id
    AND teaches.sec_id = pSec_id;
END //
DELIMITER ;

--MODIFY PERSONAL INFO
DELIMITER //
CREATE PROCEDURE updateUsername (
    IN pID VARCHAR(5),
    IN pUsername VARCHAR(30)
)
BEGIN
    UPDATE accounts
    SET username = pUsername
    WHERE accounts.ID = pID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE changePassword (
    IN pID VARCHAR(5),
    IN pPassword VARCHAR(255)
)
BEGIN
    UPDATE accounts
    SET password = pPassword
    WHERE accounts.ID = pID;
END //
DELIMITER ;


--INSTRUCTOR
--ADD/REMOVE STUDENT AS ADVISOR
DELIMITER //
CREATE PROCEDURE addAdvisor (
    IN pSID VARCHAR(5),
    IN pIID VARCHAR(5)
)
BEGIN
    INSERT INTO advisor(s_ID, i_ID)
    VALUES (pSID, pIID);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE removeAdvisor (
    IN pSID VARCHAR(5),
    IN pIID VARCHAR(5)
)
BEGIN
    delete from advisor
    WHERE advisor.s_ID = pSID
    AND advisor.i_ID = PIID;
END //
DELIMITER ;

--MODIFY COURSE PREREQS
DELIMITER //
CREATE PROCEDURE addPrereq (
    IN pc_id VARCHAR(8),
    IN pp_id VARCHAR(8)
)
BEGIN
    INSERT INTO prereq(course_id, prereq_id)
    VALUES (pc_id, pp_id);
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE removePrereq (
    IN pc_id VARCHAR(8),
    IN pp_id VARCHAR(8)
)
BEGIN
    delete from prereq
    WHERE prereq.course_id = pc_id
    AND prereq.prereq_id = pp_id;
END //
DELIMITER ;

--CHECK SECTION ROSTER
DELIMITER //
CREATE PROCEDURE checkRoster (
    IN pID VARCHAR(5),
    IN cID VARCHAR(8),
    IN sID VARCHAR (8)
)
BEGIN
    select s.ID, n.first_name, n.middle_name, n.last_name, n.second_name
    from student s, teaches t, takes a, name n
    where t.ID = pID
    and t.course_id = cID
    and t.sec_id = sID
    and s.ID = a.ID
    and t.course_id = a.course_id
    and t.sec_id = a.sec_id
    and n.name_id = s.name_id;
END // 
DELIMITER ;

--CHECK WHICH SECTIONS THEY ARE TEACHING
DELIMITER //
CREATE PROCEDURE checkRoster (
    IN pID VARCHAR(5),
    IN pSemester VARCHAR(6),
    IN pYear NUMERIC(4,0)
)
BEGIN
    select *
    from teaches
    where teaches.ID = pID
    and teaches.semester = pSemester
    and teaches.year = pYear;
END // 
DELIMITER ;

--STUDENT
--CHECK FINAL GRADES
DELIMITER //
CREATE PROCEDURE checkFinalGrades (
    IN pID VARCHAR(5)
)
BEGIN
    select *
    from takes
    where takes.ID = pID;
END // 
DELIMITER ;

--CHECK COURSES BASED ON SEMESTER
DELIMITER //
CREATE PROCEDURE checkCourses (
    IN pID VARCHAR(5),
    IN pSemester VARCHAR(6),
    IN pYear NUMERIC(4,0)
)
BEGIN
    select *
    from takes
    where takes.ID = pID
    and takes.semester = pSemester
    and takes.year = pYear;
END // 
DELIMITER ;

--CHECK SECTION INFO
DELIMITER //
CREATE PROCEDURE checkSection (
    IN pID VARCHAR(5),
    IN pSemester VARCHAR(6),
    IN pYear NUMERIC(4,0)
)
BEGIN
    select s.course_id, s.sec_id, s.semester, s.year, s.building, c.room_number, s.time_slot_id
    from section s
    inner join takes t
    on t.course_id = s.course_id
    and t.semester = s.semester
    and t.year = s.year
    inner join classroom c
    on s.room_id = c.room_id
    where t.ID = pID
    and s.semester = pSemester
    and s.year = pYear;
END // 
DELIMITER ;

--CHECK ADVISOR INFO
DELIMITER //
CREATE PROCEDURE checkAdvisor (
    IN pID VARCHAR(5)
)
BEGIN
    select i.ID, n.first_name, n.middle_name, n.last_name, n.second_name, i.dept_name
    from advisor a
    inner join instructor i
    on i.ID = a.i_ID
    inner join name n
    on i.name_id = n.name_id
    where a.s_ID = pID;
END // 
DELIMITER ;

--stuff i forgot
DELIMITER //
CREATE PROCEDURE getAllCourses ()
BEGIN
    select * from course;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllStudents ()
BEGIN
    select s.ID, n.first_name, n.middle_name, n.last_name, n.second_name, s.dept_name
    from student s
    inner join name n
    on s.name_id = n.name_id;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllInstructors ()
BEGIN
    select s.ID, n.first_name, n.middle_name, n.last_name, n.second_name, s.dept_name, s.salary
    from instructor s
    inner join name n
    on s.name_id = n.name_id;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllDepts ()
BEGIN
    select * from department;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllClassrooms ()
BEGIN
    select * from classroom;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllSections ()
BEGIN
    select * from section;
END // 
DELIMITER ;

DELIMITER //
CREATE PROCEDURE getAllTimeslots ()
BEGIN
    select * from time_slot;
END // 
DELIMITER ;

--EXTRA
--GET AVERAGE GRADE OF ALL STUDENTS IN DEPARTMENT
--GET AVERAGE GRADE OF A CLASS ACROSS RANGE OF SEMESTERS
--SHOW BEST AND WORST PERFORMING CLASSES (BY GRADES) ON SEMESTER
--SHOW TOTAL STUDENTS (PAST AND CURRENT) BY DEPARTMENT
--SHOW CURRENT STUDENTS BY DEPARTMENT