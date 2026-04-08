--INSTRUCTOR CRUD

--Instructor Create

CREATE PROCEDURE createInstructor (
IN pID VARCHAR(5),
IN pName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pSalary DECIMAL(8,2)
)
BEGIN
    INSERT INTO instructor (ID, name, dept_name, salary)
    VALUES (pID, pName, pDept_name, pSalary);
END


--Instructor Read

CREATE PROCEDURE findInstructor (
    IN pID VARCHAR(5)
)
BEGIN
    SELECT * FROM INSTRUCTOR
    WHERE instructor.ID = pID;
END

--Instructor Update

CREATE PROCEDURE updateInstructorName (
    IN pID VARCHAR(5),
    IN pName VARCHAR(20)
)
BEGIN
    UPDATE instructor
    SET name = pName
    WHERE instructor.ID = pID;
END

CREATE PROCEDURE updateInstructorSalary (
    IN pID VARCHAR(5),
    IN pSalary DECIMAL(8,2)
)
BEGIN
    UPDATE instructor
    SET salary = pSalary
    WHERE instructor.ID = pID;
END

CREATE PROCEDURE updateInstructorDept (
    IN pID VARCHAR(5),
    IN pDept_name VARCHAR(20)
)
BEGIN
    UPDATE Instructor
    SET dept_name = pDept_name
    WHERE instructor.ID = pID;
END



--Instructor Delete

CREATE PROCEDURE deleteInstructor (
    In pID VARCHAR(5)
)
BEGIN
    delete from instructor
    where instructor.ID = pID;
END

--STUDENT CRUD


--Student Create

CREATE PROCEDURE createStudent (
IN pID VARCHAR(5),
IN pName VARCHAR(20),
IN pDept_name VARCHAR(20),
IN pTot_cred DECIMAL(3,0)
)
BEGIN
    INSERT INTO student (ID, name, dept_name, tot_cred)
    VALUES (pID, pName, pDept_name, pTot_cred);
END

--Student Read

CREATE PROCEDURE findStudent (
    In pID VARCHAR(5)
)
BEGIN
    SELECT * FROM instructor
    where student.ID = pID;
END

--Student Update

CREATE PROCEDURE updateStudentName (
    IN pID VARCHAR(5),
    IN pName VARCHAR(20)
)
BEGIN
    UPDATE student
    SET name = pName
    WHERE student.ID = pID;
END

CREATE PROCEDURE updateStudentDept (
    IN pID VARCHAR(5),
    IN pDept_name VARCHAR(20)
)
BEGIN
    UPDATE student
    SET dept_name = pDept_name
    WHERE student.ID = pID;
END


--Student Delete

CREATE PROCEDURE deleteStudent (
    IN pID VARCHAR(5)
)
BEGIN
    DELETE FROM student
    WHERE student.ID = pID;
END

--SECTION CRUD


--Section Create

CREATE PROCEDURE createSection (
IN pCourse_id VARCHAR(8),
IN pSec_id VARCHAR(8),
IN pSemester VARCHAR(6),
IN pYear DECIMAL(4,0)
IN pBuilding VARCHAR(15),
IN pRoom_number VARCHAR(7),
IN pTime_slot_id VARCHAR(4)
)
BEGIN
    INSERT INTO section (course_id, sec_id, semester, year, building, room_number, time_slot_id)
    VALUES (pCourse_id, pSec_id, pSemester, pYear, pBuilding, pRoom_number, pTime_slot_id);
END


--Section Read (Find all sections of a class)

CREATE PROCEDURE findSectionsOfClass (
    IN pCourse_id VARCHAR(8)
)
BEGIN
    SELECT * FROM section
    WHERE section.course_id = pCourse_id;
END

--Section Update

CREATE PROCEDURE updateSectionBuilding (
    IN pSec_id VARCHAR(8),
    IN pBuilding VARCHAR(15)
)
BEGIN
    UPDATE section
    SET building = pBuilding
    WHERE section.sec_id = pSec_id;
END

CREATE PROCEDURE updateSectionRoomNumber (
    IN pSec_id VARCHAR(8),
    IN pRoom_number VARCHAR(7)
)
BEGIN
    UPDATE section
    SET room_number = pRoom_number
    WHERE section.sec_id = pSec_id;
END


CREATE PROCEDURE updateTimeSlotId (
    IN pSec_id VARCHAR(8),
    IN pTime_slot_id VARCHAR(4)
)
BEGIN
    UPDATE section
    SET time_slot_id = pTime_slot_id
    WHERE section.sec_id = pSec_id;
END

--Section Delete

CREATE PROCEDURE deleteSection (
    In pSec_id VARCHAR(5)
)
BEGIN
    delete from section
    where section.sec_id = pSec_id;
END

--Enroll in a Class

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
END

--Assign Instructor to Class

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
END


--Drop a Section for a student

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
END

--Give a Grade to a Section for a student

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
END