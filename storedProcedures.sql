--INSTRUCTOR CRUD

--Instructor Create

DELIMITER //
CREATE PROCEDURE createInstructor (
IN pID VARCHAR(5),
IN nID VARCHAR(5),
IN pFirstName VARCHAR(20),
IN pMiddleName VARCHAR(20),
IN pLastName VARCHAR(20),
IN pSecondName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pSalary DECIMAL(8,2),
IN pUsername VARCHAR(30),
IN pPassword VARCHAR(255)
)
BEGIN
    INSERT INTO name (name_id, first_name, middle_name, last_name, second_name)
    VALUES (nID, pFirstName, pMiddleName, pLastName, pSecondName);
    INSERT INTO accounts (ID, username, password, permission)
    VALUES (pID, pUsername, pPassword, 'Instructor');
    INSERT INTO instructor (ID, name_id, dept_name, salary)
    VALUES (pID, nID, pDept_name, pSalary);
END //
DELIMITER ;


--Instructor Read

DELIMITER //
CREATE PROCEDURE findInstructor (
    IN pID VARCHAR(5)
)
BEGIN
    SELECT * FROM instructor as i, name as n
    WHERE i.ID = pid
    AND i.name_id = n.name_id;
END //
DELIMITER ;

--Instructor Update

DELIMITER //
CREATE PROCEDURE updateInstructorName (
    IN pID VARCHAR(5),
    IN pFirstName VARCHAR(20),
    IN pMiddleName VARCHAR(20),
    IN pLastName VARCHAR(20),
    IN pSecondName VARCHAR(20)
)
BEGIN
    UPDATE name
    SET first_name = pFirstName,
    	middle_name = pMiddleName,
    	last_name = pLastName,
    	second_name = pSecondName
    WHERE name_id = (
        SELECT name_id
        FROM instructor
        WHERE ID = pID
    );
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateInstructorSalary (
    IN pID VARCHAR(5),
    IN pSalary DECIMAL(8,2)
)
BEGIN
    UPDATE instructor
    SET salary = pSalary
    WHERE instructor.ID = pID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateInstructorDept (
    IN pID VARCHAR(5),
    IN pDept_name VARCHAR(20)
)
BEGIN
    UPDATE instructor
    SET dept_name = pDept_name
    WHERE instructor.ID = pID;
END //
DELIMITER ;



--Instructor Delete

DELIMITER //
CREATE PROCEDURE deleteInstructor (
    IN pID VARCHAR(5)
)
BEGIN
    DELETE i, n, a, t, d
    FROM instructor i
    INNER JOIN name n ON i.name_id = n.name_id
    INNER JOIN accounts a on i.ID = a.ID
    INNER JOIN teaches t on i.ID = t.ID
    INNER JOIN advisor d on i.ID = d.i_ID
    WHERE i.ID = pID;
END //
DELIMITER ;

--STUDENT CRUD


--Student Create

DELIMITER //
CREATE PROCEDURE createStudent (
IN pID VARCHAR(5),
IN nID VARCHAR(5),
IN pFirstName VARCHAR(20),
IN pMiddleName VARCHAR(20),
IN pLastName VARCHAR(20),
IN pSecondName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pUsername VARCHAR(30),
IN pPassword VARCHAR(255)
)
BEGIN
    INSERT INTO name (name_id, first_name, middle_name, last_name, second_name)
    VALUES (nID, pFirstName, pMiddleName, pLastName, pSecondName);
    INSERT INTO accounts (ID, username, password, permission)
    VALUES (pID, pUsername, pPassword, 'Student');
    INSERT INTO student (ID, name_id, dept_name)
    VALUES (pID, nID, pDept_name);
END //
DELIMITER ;

--Student Read

DELIMITER //
CREATE PROCEDURE findStudent (
    IN pID VARCHAR(5)
)
BEGIN
    SELECT * FROM student as i, name as n
    WHERE i.ID = pid
    AND i.name_id = n.name_id;
END //
DELIMITER ;

--Student Update

DELIMITER //
CREATE PROCEDURE updateStudentName (
    IN pID VARCHAR(5),
    IN pName VARCHAR(20)
)
BEGIN
    UPDATE student
    SET name = pName
    WHERE student.ID = pID;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateStudentDept (
    IN pID VARCHAR(5),
    IN pDept_name VARCHAR(20)
)
BEGIN
    UPDATE student
    SET dept_name = pDept_name
    WHERE student.ID = pID;
END //
DELIMITER ;

--Student Delete

DELIMITER //
CREATE PROCEDURE deleteStudent (
    IN pID VARCHAR(5)
)
BEGIN
    DELETE i, n, a, t, d
    FROM student i
    INNER JOIN name n ON i.name_id = n.name_id
    INNER JOIN accounts a on i.ID = a.ID
    INNER JOIN takes t on i.ID = t.ID
    INNER JOIN advisor d on i.ID = d.s_ID
    WHERE i.ID = pID;
END //
DELIMITER ;

--SECTION CRUD


--Section Create

DELIMITER //
CREATE PROCEDURE createSection (
IN pCourse_id VARCHAR(8),
IN pSec_id VARCHAR(8),
IN pSemester VARCHAR(6),
IN pYear DECIMAL(4,0),
IN pBuilding VARCHAR(15),
IN pRoom_id VARCHAR(7),
IN pTime_slot_id VARCHAR(4)
)
BEGIN
    INSERT INTO section (course_id, sec_id, semester, year, building, room_id, time_slot_id)
    VALUES (pCourse_id, pSec_id, pSemester, pYear, pBuilding, pRoom_id, pTime_slot_id);
END //
DELIMITER ;


--Section Read (Find all sections of a class)

DELIMITER //
CREATE PROCEDURE findSectionsOfClass (
    IN pCourse_id VARCHAR(8)
)
BEGIN
    SELECT * FROM section
    WHERE section.course_id = pCourse_id;
END //
DELIMITER ;

--Section Update

DELIMITER //
CREATE PROCEDURE updateSectionBuilding (
    IN pSec_id VARCHAR(8),
    IN pBuilding VARCHAR(15)
)
BEGIN
    UPDATE section
    SET building = pBuilding
    WHERE section.sec_id = pSec_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateSectionRoomID (
    IN pSec_id VARCHAR(8),
    IN pRoom_id VARCHAR(7)
)
BEGIN
    UPDATE section
    SET room_id = pRoom_id
    WHERE section.sec_id = pSec_id;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE updateTimeSlotId (
    IN pSec_id VARCHAR(8),
    IN pTime_slot_id VARCHAR(4)
)
BEGIN
    UPDATE section
    SET time_slot_id = pTime_slot_id
    WHERE section.sec_id = pSec_id;
END //
DELIMITER ;

--Section Delete

DELIMITER //
CREATE PROCEDURE deleteSection (
    In pSec_id VARCHAR(5),
    In pCourse_id VARCHAR(8)
)
BEGIN
    delete from section
    where section.sec_id = pSec_id
    and section.course_id = pCourse_id;
END //
DELIMITER ;

--Enroll in a Class

DELIMITER //
CREATE PROCEDURE classEnroll (
    IN pStudent_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8),
    IN pSemester VARCHAR(6),
    IN pYear DECIMAL(4,0)
)
BEGIN
    INSERT INTO takes (ID, course_id, sec_id, semester, year)
    VALUES (pStudent_id, pCourse_id, pSec_id, pSemester, pYear);
END //
DELIMITER ;

--Assign Instructor to Class

DELIMITER //
CREATE PROCEDURE assignInstructor (
    IN pInstructor_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8),
    IN pSemester VARCHAR(6),
    IN pYear DECIMAL(4,0)
)
BEGIN
    INSERT INTO teaches (ID, course_id, sec_id, semester, year)
    VALUES (pInstructor_id, pCourse_id, pSec_id, pSemester, pYear);
END //
DELIMITER ;


--Drop a Section for a student

DELIMITER //
CREATE PROCEDURE dropSection (
    IN pStudent_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8),
    IN pSemester VARCHAR(6),
    IN pYear DECIMAL(4,0)
)
BEGIN
    DELETE FROM takes
    WHERE ID = pStudent_id
    AND course_id = pCourse_id
    AND sec_id = pSec_id
    AND semester = pSemester
    AND year = pYear;
END //
DELIMITER ;

--Give a Grade to a Section for a student

DELIMITER //
CREATE PROCEDURE gradeSection (
    IN pStudent_id VARCHAR(5),
    IN pCourse_id VARCHAR(8),
    IN pSec_id VARCHAR(8),
    IN pSemester VARCHAR(6),
    IN pYear DECIMAL(4,0),
    IN pGrade VARCHAR(2)
)
BEGIN
    UPDATE takes
    SET grade = pGrade
    WHERE ID = pStudent_id
    AND course_id = pCourse_id
    AND sec_id = pSec_id
    AND semester = pSemester
    AND year = pYear;
END //
DELIMITER ;