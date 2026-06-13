class BubbleSort:

    complexity = "O(n²)"

    @staticmethod
    def sort(students, key_name="nim"):

        data = students[:]

        n = len(data)

        for i in range(n):

            for j in range(0, n - i - 1):

                if getattr(data[j], key_name) > getattr(data[j + 1], key_name):

                    data[j], data[j + 1] = (data[j + 1], data[j])

        return data


class SelectionSort:

    complexity = "O(n²)"

    @staticmethod
    def sort(students, key_name="nim"):

        data = students[:]

        n = len(data)

        for i in range(n):

            min_idx = i

            for j in range(i + 1, n):

                if getattr(data[j], key_name) < getattr(data[min_idx], key_name):

                    min_idx = j

            data[i], data[min_idx] = (data[min_idx], data[i])

        return data


class MergeSort:

    complexity = "O(n log n)"

    @staticmethod
    def sort(students, key_name="nim"):

        if len(students) <= 1:

            return students

        middle = len(students) // 2

        left = MergeSort.sort(students[:middle], key_name)

        right = MergeSort.sort(students[middle:], key_name)

        return MergeSort.merge(left, right, key_name)

    @staticmethod
    def merge(left, right, key_name):

        result = []

        i = 0
        j = 0

        while i < len(left) and j < len(right):

            if getattr(left[i], key_name) <= getattr(right[j], key_name):

                result.append(left[i])

                i += 1

            else:

                result.append(right[j])

                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result
